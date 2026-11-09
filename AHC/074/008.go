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
	level [65]uint8
	core  [65]bool
}

func newTarget(bits uint64, n int) Target {
	t := Target{bits: bits}
	next := n - 1
	t.core[n] = bits>>(n-1)&1 != 0
	if t.core[n] {
		next = n
	}
	t.level[n] = uint8(next)
	for k := n - 1; k >= 0; k-- {
		t.core[k] = bits>>k&1 == 0
		if t.core[k] {
			next = k
		}
		t.level[k] = uint8(next)
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

// A retained paper cannot cover any required paper still below it. Among the
// remaining papers, a required paper conflicts only with optional papers at the
// same target level. Moving that one required paper is optimal; if just one
// optional paper precedes it, either paper can move at the same cost.
func solveChoice(order []int, t *Target, ties uint64) Choice {
	n := len(order) - 1
	future, level := n+1, uint8(n+1)
	core, first, count := 0, 0, 0
	var choice Choice
	mark := func(k int, on bool) {
		if k == n {
			choice.last = on
		} else if on {
			choice.moved |= uint64(1) << k
		} else {
			choice.moved &^= uint64(1) << k
		}
	}
	for pos := n; pos >= 0; pos-- {
		k := order[pos]
		strength := min(k, n-1) + 1
		if strength >= future {
			mark(k, true)
			choice.cost++
			continue
		}
		if t.core[k] {
			future, level, core, count = strength, t.level[k], k, 0
		} else if t.level[k] == level {
			if count == 0 {
				first = k
				if ties>>uint(core%64)&1 != 0 {
					first = core
				}
				mark(first, true)
				choice.cost++
			} else if count == 1 {
				mark(first, false)
				mark(core, true)
			}
			count++
		}
	}
	return choice
}

func solve(order []int, t *Target) Choice {
	return solveChoice(order, t, 0)
}

// The same reverse scan needs only a count when no path is being reconstructed.
func solveCost(order []int, t *Target) int {
	n := len(order) - 1
	future, level, kept := n+1, uint8(n+1), 0
	coreKept := false
	for pos := n; pos >= 0; pos-- {
		k := order[pos]
		strength := min(k, n-1) + 1
		if strength >= future {
			continue
		}
		kept++
		if t.core[k] {
			future, level, coreKept = strength, t.level[k], true
		} else if coreKept && t.level[k] == level {
			kept--
			coreKept = false
		}
	}
	return len(order) - kept
}

type Move struct{ paper, depth int }
type Candidate struct {
	order []int
	moves []Move
	sum   int
}

type Evaluation struct {
	candidates []Candidate
	request    int
	sums       []int
	deadline   time.Time
	cpuEnd     time.Duration
}

func evaluateCandidate(c Candidate, targets []Target, task Evaluation) int {
	sum := 0
	for query := range targets {
		if query%64 == 0 && expired(task.deadline, task.cpuEnd) {
			return 1 << 30
		}
		if query != task.request {
			sum += solveCost(c.order, &targets[query])
		}
	}
	return sum
}

// Workers read immutable orders and write disjoint result slots.
func startEvaluators(targets []Target, workers int) ([]chan Evaluation, chan struct{}) {
	jobs := make([]chan Evaluation, workers)
	done := make(chan struct{}, workers)
	for w := range jobs {
		jobs[w] = make(chan Evaluation)
		go func(w int) {
			defer func() { done <- struct{}{} }()
			for task := range jobs[w] {
				for i := w; i < len(task.candidates); i += workers {
					task.sums[i] = evaluateCandidate(task.candidates[i], targets, task)
				}
				done <- struct{}{}
			}
		}(w)
	}
	return jobs, done
}

func evaluate(jobs []chan Evaluation, done chan struct{}, task Evaluation) {
	for _, job := range jobs {
		job <- task
	}
	for range jobs {
		<-done
	}
}

// Every completed score averages all possible next products, excluding the
// current request. An interrupted score cannot compete with a complete score.
func choose(candidates []Candidate, targets []Target, request int,
	jobs []chan Evaluation, done chan struct{}, deadline time.Time, cpuEnd time.Duration) int {
	best := bestCandidate(candidates, 1)
	if len(candidates) == 1 || len(targets) <= 1 || expired(deadline, cpuEnd) {
		return best
	}
	sums := make([]int, len(candidates))
	evaluate(jobs, done, Evaluation{candidates: candidates, request: request, sums: sums,
		deadline: deadline, cpuEnd: cpuEnd})
	if slices.Min(sums) == 1<<30 {
		return best
	}
	for i := range candidates {
		candidates[i].sum = sums[i]
	}
	return bestCandidate(candidates, len(targets)-1)
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

// Sample the independent equal-cost choices instead of taking the first few
// masks in numerical order. Include both extremes and deduplicate before build.
func expandedCandidates(order []int, t *Target, limit int) []Candidate {
	candidates := candidatesFor(order, t)
	base := solve(order, t)
	choices := make([]Choice, 0, 8)
	for i := uint64(1); i < 8; i++ {
		x := t.bits + i*0x9e3779b97f4a7c15
		x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9
		x = (x ^ (x >> 27)) * 0x94d049bb133111eb
		x ^= x >> 31
		if i == 1 {
			x = ^uint64(0)
		}
		choice := solveChoice(order, t, x)
		if choice != base && !slices.Contains(choices, choice) {
			choices = append(choices, choice)
		}
	}
	for mode := 0; mode < 4 && len(candidates) < limit; mode++ {
		for _, choice := range choices {
			c, ok := build(order, t, choice, mode)
			if ok && !slices.ContainsFunc(candidates, func(old Candidate) bool { return slices.Equal(c.order, old.order) }) {
				candidates = append(candidates, c)
				if len(candidates) == limit {
					break
				}
			}
		}
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
		var candidates []Candidate
		best := 0
		if turn+1 < r {
			candidates = expandedCandidates(order, &targets[request], 24)
			best = choose(candidates, targets, request, jobs, done, deadline, cpuDeadline)
		} else {
			candidates = candidatesFor(order, &targets[request])
			best = bestCandidate(candidates, 1)
		}
		chosen := candidates[best]
		order = chosen.order
		spent += time.Since(begin)
		fmt.Fprintln(out, len(chosen.moves))
		for _, m := range chosen.moves {
			fmt.Fprintln(out, m.paper, m.depth)
		}
		out.Flush()
	}
}
