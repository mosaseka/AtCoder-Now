package main

import (
	"bufio"
	"fmt"
	"math"
	"math/rand"
	"os"
	"runtime"
	"slices"
	"syscall"
	"time"
)

const (
	totalBudget       = 1800 * time.Millisecond
	designBudget      = 1000 * time.Millisecond
	screeningBudget   = 650 * time.Millisecond
	restartsPerWorker = 32
)

type Target struct {
	bits  uint64
	level [65]int
	core  [65]bool
	keep  [65]uint64 // Eligible retained maxima when keeping each paper.
}

func newTarget(bits uint64, n int) Target {
	t := Target{bits: bits}
	rank := -1
	for k := 0; k < n; k++ {
		if bits>>k&1 == 0 {
			rank++
			t.core[k], t.level[k] = true, rank
		}
	}
	if bits>>(n-1)&1 != 0 {
		rank++
		t.core[n] = true
	}
	t.level[n] = rank
	for k := n - 1; k >= 0; k-- {
		if t.core[k] {
			rank = t.level[k]
		} else {
			t.level[k] = rank
		}
	}
	previous := -1
	for k := 0; k <= n; k++ {
		if t.core[k] {
			t.keep[k] = uint64(1)<<(previous+1) - 1
			previous = k
		} else {
			t.keep[k] = uint64(1)<<min(k, n-1) - 1
		}
	}
	return t
}

func (t *Target) before(a, b int) bool {
	return t.core[a] && (t.level[a] < t.level[b] || !t.core[b] && t.level[a] == t.level[b])
}

type Choice struct {
	moved uint64
	cost  uint8
	last  bool // Paper N needs a separate bit when N == 64.
}

func better(a, b Choice) bool {
	return a.cost < b.cost || a.cost == b.cost &&
		(!a.last && b.last || a.last == b.last && a.moved < b.moved)
}

// Keeping the strongest paper also fixes the highest retained target level.
func solve(order []int, t *Target) Choice {
	n := len(order) - 1
	var states [65]Choice
	for m := 1; m <= n; m++ {
		states[m].cost = 255
	}
	for _, k := range order {
		strength, best := min(k, n-1)+1, Choice{cost: 255}
		for maximum := 0; maximum < strength; maximum++ {
			value := states[maximum]
			if value.cost == 255 {
				continue
			}
			if (!t.core[k] || maximum == 0 || t.level[maximum-1] < t.level[k]) && better(value, best) {
				best = value
			}
			value.cost++
			if k == n {
				value.last = true
			} else {
				value.moved |= uint64(1) << k
			}
			states[maximum] = value
		}
		if t.core[k] {
			for maximum := strength; maximum <= n; maximum++ {
				states[maximum].cost = 255
			}
		}
		if better(best, states[strength]) {
			states[strength] = best
		}
	}
	best := Choice{cost: 255}
	for _, value := range states[:n+1] {
		if better(value, best) {
			best = value
		}
	}
	return best
}

// Seven bit planes store the costs of retained maxima 1..64. State zero
// (no retained paper) is separate; invalid states never participate in minima.
type CostBits [7]uint64

func (c *CostBits) minimum(valid uint64) int {
	if valid == 0 {
		return 127
	}
	value := 0
	for bit := 6; bit >= 0; bit-- {
		zeros := valid &^ c[bit]
		if zeros != 0 {
			valid = zeros
		} else {
			value |= 1 << bit
		}
	}
	return value
}

func solveCost(order []int, t *Target) int {
	n := len(order) - 1
	var costs CostBits
	var valid uint64
	for zero, k := range order {
		strength := min(k, n-1)
		bit := uint64(1) << strength
		low := bit - 1
		best := min(zero, costs.minimum(valid&t.keep[k]))
		carry := valid & low
		for b := 0; carry != 0; b++ {
			next := costs[b] & carry
			costs[b] ^= carry
			carry = next
		}
		if t.core[k] {
			valid &= low
		}
		if valid&bit == 0 || best < costs.minimum(bit) {
			valid |= bit
			for b := range costs {
				costs[b] &^= bit
				if best>>b&1 != 0 {
					costs[b] |= bit
				}
			}
		}
	}
	return min(len(order), costs.minimum(valid))
}

type Move struct{ paper, depth int }
type Candidate struct {
	order []int
	moves []Move
	sum   int
}

type Evaluation struct {
	candidates []Candidate
	queries    []int
	sums       []int
}

// Workers use local DP arrays; candidate orders and targets are read-only.
func startEvaluators(targets []Target, workers int) ([]chan Evaluation, chan struct{}) {
	jobs := make([]chan Evaluation, workers)
	done := make(chan struct{}, workers)
	for w := range jobs {
		jobs[w] = make(chan Evaluation)
		go func(w int) {
			defer func() { done <- struct{}{} }()
			for task := range jobs[w] {
				for i := w; i < len(task.candidates); i += workers {
					sum := 0
					for _, query := range task.queries {
						sum += solveCost(task.candidates[i].order, &targets[query])
					}
					task.sums[i] = sum
				}
				done <- struct{}{}
			}
		}(w)
	}
	return jobs, done
}

func cpuTime() time.Duration {
	var usage syscall.Rusage
	syscall.Getrusage(syscall.RUSAGE_SELF, &usage)
	return time.Duration(usage.Utime.Sec+usage.Stime.Sec)*time.Second +
		time.Duration(usage.Utime.Usec+usage.Stime.Usec)*time.Microsecond
}

func move(order []int, from, depth int) {
	k := order[from]
	if from < depth {
		copy(order[from:depth], order[from+1:depth+1])
	} else {
		copy(order[depth+1:from+1], order[depth:from])
	}
	order[depth] = k
}

func build(order []int, t *Target, choice Choice, mode int) (Candidate, bool) {
	c := Candidate{order: slices.Clone(order), moves: make([]Move, 0, int(choice.cost))}
	n := len(order) - 1
	pending := func(k int) bool {
		if k == n {
			return choice.last
		}
		return choice.moved>>k&1 != 0
	}
	for len(c.moves) < int(choice.cost) {
		var visible [65]int
		count, covered := 0, -1
		for pos, k := range c.order {
			strength := min(k, n-1)
			if strength > covered && pending(k) {
				visible[count] = pos
				count++
			}
			covered = max(covered, strength)
		}
		found := false
		for i := 0; i < count; i++ {
			at := i
			if mode == 2 {
				at = count - 1 - i
			}
			from := visible[at]
			k := c.order[from]
			if k == n {
				choice.last = false
			} else {
				choice.moved &^= uint64(1) << k
			}
			low, high, pos := 0, n, 0
			for _, x := range c.order {
				if x == k {
					continue
				}
				if pending(x) {
					if min(x, n-1) <= min(k, n-1) {
						low = max(low, pos+1)
					}
				} else {
					if t.before(x, k) {
						low = max(low, pos+1)
					}
					if t.before(k, x) {
						high = min(high, pos)
					}
				}
				pos++
			}
			if low <= high {
				depth := low
				if mode == 0 || mode == 2 {
					depth = min(high, max(low, from))
				} else if mode == 3 {
					depth = min(low+1, high)
				}
				move(c.order, from, depth)
				c.moves = append(c.moves, Move{k, depth})
				found = true
				break
			}
			if k == n {
				choice.last = true
			} else {
				choice.moved |= uint64(1) << k
			}
		}
		if !found {
			return c, false
		}
	}
	return c, display(c.order) == t.bits
}

func display(order []int) uint64 {
	n, covered := len(order)-1, -1
	value := ^uint64(0) >> (64 - n)
	for _, k := range order {
		strength := min(k, n-1)
		if strength > covered && k < n {
			value &^= uint64(1) << k
		}
		covered = max(covered, strength)
	}
	return value
}

// Guaranteed legal fallback: sort the active papers, then hide unwanted zeros.
func fallback(order []int, t *Target) Candidate {
	c := Candidate{order: slices.Clone(order)}
	n := len(order) - 1
	apply := func(k, depth int) {
		from := slices.Index(c.order, k)
		if from != depth {
			move(c.order, from, depth)
			c.moves = append(c.moves, Move{k, depth})
		}
	}
	if slices.Index(c.order, n-1) < slices.Index(c.order, n) {
		apply(n-1, slices.Index(c.order, n))
	}
	for k := n; k > 0; k-- {
		apply(k, k)
	}
	for k := 0; k < n; k++ {
		if t.bits>>k&1 != 0 {
			apply(k, n)
		}
	}
	return c
}

func candidatesFor(order []int, t *Target) []Candidate {
	choice := solve(order, t)
	candidates := make([]Candidate, 0, 4)
	for mode := 0; mode < 4; mode++ {
		c, ok := build(order, t, choice, mode)
		if ok && !slices.ContainsFunc(candidates, func(old Candidate) bool { return slices.Equal(c.order, old.order) }) {
			candidates = append(candidates, c)
		}
	}
	if len(candidates) == 0 {
		candidates = append(candidates, fallback(order, t))
	}
	return candidates
}

func bestCandidate(candidates []Candidate, weight int) int {
	best := 0
	for i := 1; i < len(candidates); i++ {
		a, b := &candidates[i], &candidates[best]
		sa, sb := len(a.moves)*weight+a.sum, len(b.moves)*weight+b.sum
		if sa < sb || sa == sb && (len(a.moves) < len(b.moves) ||
			len(a.moves) == len(b.moves) && slices.Compare(a.order, b.order) < 0) {
			best = i
		}
	}
	return best
}

type Design struct {
	order []int
	flip  uint64 // Indexed by original window, before applying the permutation.
}

func (d Design) targets(patterns []uint64) []Target {
	targets := make([]Target, len(patterns))
	for i, bits := range patterns {
		var reordered uint64
		for j, original := range d.order {
			reordered |= ((bits ^ d.flip) >> original & 1) << j
		}
		targets[i] = newTarget(reordered, len(d.order))
	}
	return targets
}

func (d Design) paper(k int) string {
	n := len(d.order)
	s := make([]byte, n)
	for j := range s {
		s[j] = '.'
	}
	if k <= n {
		for j := 0; j < min(k+1, n); j++ {
			bit := uint64(1)
			if j == k {
				bit = 0
			}
			original := d.order[j]
			s[original] = '0' + byte(bit^(d.flip>>original&1))
		}
	}
	return string(s)
}

func expired(wall time.Time, cpu time.Duration) bool {
	return !time.Now().Before(wall) || cpuTime() >= cpu
}

type Path struct {
	order []int
	cost  int
}

// Two independent searches keep the best path from each restart.
func searchPaths(distance *[64][64]int, n int, wall time.Time, cpu time.Duration) []Path {
	paths := make([]Path, 2*restartsPerWorker)
	done := make(chan struct{}, 2)
	for worker := 0; worker < 2; worker++ {
		go func(w int) {
			defer func() { done <- struct{}{} }()
			rng := rand.New(rand.NewSource(int64(74 + w)))
			for restart := 0; restart < restartsPerWorker; restart++ {
				order := rng.Perm(n)
				score := 0
				for i := 1; i < n; i++ {
					score += distance[order[i-1]][order[i]]
				}
				best := Path{slices.Clone(order), score}
				for iteration := 0; iteration < 25000; iteration++ {
					if iteration%1024 == 0 && expired(wall, cpu) {
						break
					}
					left, right := rng.Intn(n), rng.Intn(n)
					if left > right {
						left, right = right, left
					}
					delta := 0
					if left > 0 {
						delta += distance[order[left-1]][order[right]] - distance[order[left-1]][order[left]]
					}
					if right+1 < n {
						delta += distance[order[left]][order[right+1]] - distance[order[right]][order[right+1]]
					}
					if delta <= 0 || iteration < 18000 && rng.Float64() < math.Exp(-float64(delta)/(8*(1-float64(iteration)/18000))) {
						slices.Reverse(order[left : right+1])
						score += delta
						if score < best.cost {
							best = Path{slices.Clone(order), score}
						}
					}
				}
				paths[w*restartsPerWorker+restart] = best
				if expired(wall, cpu) {
					break
				}
			}
		}(worker)
	}
	<-done
	<-done
	return slices.DeleteFunc(paths, func(p Path) bool { return p.order == nil })
}

func mockRequests(p, count int, seed int64) []int {
	rng := rand.New(rand.NewSource(seed))
	requests := make([]int, 32+count)
	for i := range requests {
		requests[i] = rng.Intn(p)
		if i > 0 && p > 1 {
			requests[i] = rng.Intn(p - 1)
			if requests[i] >= requests[i-1] {
				requests[i]++
			}
		}
	}
	return requests
}

// Incomplete simulations have infinite cost and never compete with full runs.
func evaluateDesigns(designs []Design, indices []int, patterns []uint64, requests []int, wall time.Time, cpu time.Duration) []int {
	const infinity = 1 << 30
	scores := make([]int, len(designs))
	for i := range scores {
		scores[i] = infinity
	}
	done := make(chan struct{}, 2)
	for worker := 0; worker < 2; worker++ {
		go func(w int) {
			defer func() { done <- struct{}{} }()
			for at := w; at < len(indices); at += 2 {
				if expired(wall, cpu) {
					return
				}
				i := indices[at]
				targets := designs[i].targets(patterns)
				order := make([]int, len(designs[i].order)+1)
				for k := range order {
					order[k] = k
				}
				total := 0
				for turn, request := range requests {
					if turn%8 == 0 && expired(wall, cpu) {
						return
					}
					candidates := candidatesFor(order, &targets[request])
					chosen := candidates[bestCandidate(candidates, 1)]
					order = chosen.order
					if turn >= 32 {
						total += len(chosen.moves)
					}
				}
				scores[i] = total
			}
		}(worker)
	}
	<-done
	<-done
	return scores
}

func design(patterns []uint64, n int) Design {
	begin, cpu := time.Now(), cpuTime()
	wallEnd, cpuEnd := begin.Add(designBudget), cpu+designBudget
	var distance, signed [64][64]int
	for i := 0; i < n; i++ {
		for j := 0; j < i; j++ {
			for _, bits := range patterns {
				distance[i][j] += int((bits>>i ^ bits>>j) & 1)
			}
			distance[j][i] = distance[i][j]
			signed[i][j] = min(distance[i][j], len(patterns)-distance[i][j])
			signed[j][i] = signed[i][j]
		}
	}
	paths := searchPaths(&distance, n, wallEnd, cpuEnd)
	baseline := paths[0]
	for _, path := range paths[1:] {
		if path.cost < baseline.cost || path.cost == baseline.cost && slices.Compare(path.order, baseline.order) < 0 {
			baseline = path
		}
	}
	designs := []Design{{order: baseline.order}}
	paths = searchPaths(&signed, n, wallEnd, cpuEnd)
	slices.SortFunc(paths, func(a, b Path) int {
		if a.cost != b.cost {
			return a.cost - b.cost
		}
		return slices.Compare(a.order, b.order)
	})
	// Limit simulation work to the eight best paths (up to 32 signed designs).
	for _, path := range paths[:min(8, len(paths))] {
		var flip uint64
		for j := 1; j < n; j++ {
			a, b := path.order[j-1], path.order[j]
			bit := flip >> a & 1
			if distance[a][b] > len(patterns)/2 {
				bit ^= 1
			}
			flip |= bit << b
		}
		for reverse := 0; reverse < 2; reverse++ {
			order := slices.Clone(path.order)
			if reverse != 0 {
				slices.Reverse(order)
			}
			for complement := 0; complement < 2; complement++ {
				mask := flip
				if complement != 0 {
					mask ^= ^uint64(0) >> (64 - n)
				}
				candidate := Design{order, mask}
				if !slices.ContainsFunc(designs, func(d Design) bool { return d.flip == mask && slices.Equal(d.order, order) }) {
					designs = append(designs, candidate)
				}
			}
		}
	}
	indices := make([]int, len(designs))
	for i := range indices {
		indices[i] = i
	}
	scores := evaluateDesigns(designs, indices, patterns, mockRequests(len(patterns), 256, 7401), begin.Add(screeningBudget), cpu+screeningBudget)
	// Stable sorting makes ties favor the baseline, then candidate generation order.
	slices.SortStableFunc(indices, func(a, b int) int { return scores[a] - scores[b] })
	best := indices[0]
	finalists := []int{0}
	for _, i := range indices {
		if i != 0 && scores[i] < 1<<30 && len(finalists) < 4 {
			finalists = append(finalists, i)
		}
	}
	scores = evaluateDesigns(designs, finalists, patterns, mockRequests(len(patterns), 1024, 7402), wallEnd, cpuEnd)
	if scores[0] < 1<<30 {
		best = 0
		for _, i := range finalists[1:] {
			if scores[i] < scores[best] {
				best = i
			}
		}
	}
	return designs[best]
}

func main() {
	workers := min(2, runtime.GOMAXPROCS(0))
	runtime.GOMAXPROCS(workers)
	in := bufio.NewReader(os.Stdin)
	out := bufio.NewWriterSize(os.Stdout, 1<<20)
	var n, k, p, r int
	fmt.Fscan(in, &n, &k, &p, &r)
	patterns := make([]uint64, p)
	for i := range patterns {
		var s string
		fmt.Fscan(in, &s)
		var bits uint64
		for j := range s {
			if s[j] == '1' {
				bits |= uint64(1) << j
			}
		}
		patterns[i] = bits
	}
	begin := time.Now()
	layout := design(patterns, n)
	targets := layout.targets(patterns)
	for paper := 0; paper < k; paper++ {
		fmt.Fprintln(out, layout.paper(paper))
	}
	out.Flush()
	order := make([]int, n+1)
	for i := range order {
		order[i] = i
	}
	jobs, done := startEvaluators(targets, workers)
	defer func() {
		for _, job := range jobs {
			close(job)
		}
		for range jobs {
			<-done
		}
	}()
	rng := rand.New(rand.NewSource(74))
	spent := time.Since(begin)
	for turn := 0; turn < r; turn++ {
		var request int
		if _, err := fmt.Fscan(in, &request); err != nil || request == -1 {
			return
		}
		begin := time.Now()
		cpu := cpuTime()
		quota := max(time.Duration(0), (totalBudget-max(spent, cpu))/time.Duration(r-turn))
		deadline, cpuDeadline := begin.Add(quota), cpu+quota
		candidates := candidatesFor(order, &targets[request])
		samples := 0
		if len(candidates) > 1 && turn+1 < r {
			next := slices.DeleteFunc(rng.Perm(p), func(q int) bool { return q == request })
			for first := 0; first < len(next); first += 4 {
				if !time.Now().Before(deadline) || cpuTime() >= cpuDeadline {
					break
				}
				last := min(first+4, len(next))
				sums := make([]int, len(candidates))
				for _, job := range jobs {
					job <- Evaluation{candidates, next[first:last], sums}
				}
				for range jobs {
					<-done
				}
				for i := range candidates {
					candidates[i].sum += sums[i]
				}
				samples += last - first
			}
		}
		chosen := candidates[bestCandidate(candidates, max(1, samples))]
		order = chosen.order
		spent += time.Since(begin)
		fmt.Fprintln(out, len(chosen.moves))
		for _, m := range chosen.moves {
			fmt.Fprintln(out, m.paper, m.depth)
		}
		out.Flush()
	}
}
