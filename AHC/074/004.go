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

type Target struct {
	bits  uint64
	level [65]int
	core  [65]bool
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

// Target levels increase with paper strength, so the retained maximum alone
// determines the stage. Cost evaluation therefore needs only N+1 states.
func solveCost(order []int, t *Target) int {
	const infinity = 1 << 20
	n := len(order) - 1
	var costs [65]int
	for m := 1; m <= n; m++ {
		costs[m] = infinity
	}
	for _, k := range order {
		strength, best := min(k, n-1)+1, infinity
		for maximum := 0; maximum < strength; maximum++ {
			if !t.core[k] || maximum == 0 || t.level[maximum-1] < t.level[k] {
				best = min(best, costs[maximum])
			}
			costs[maximum]++
		}
		if t.core[k] {
			for maximum := strength; maximum <= n; maximum++ {
				costs[maximum] = infinity
			}
		}
		costs[strength] = min(costs[strength], best)
	}
	return slices.Min(costs[:n+1])
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

// Arrange correlated windows next to each other in the prefix-paper design.
func design(patterns []uint64, n int) []int {
	var distance [64][64]int
	for i := 0; i < n; i++ {
		for j := i + 1; j < n; j++ {
			for _, bits := range patterns {
				distance[i][j] += int((bits>>i ^ bits>>j) & 1)
			}
			distance[j][i] = distance[i][j]
		}
	}
	type result struct {
		order []int
		score int
	}
	done := make(chan result, 2)
	for worker := 0; worker < 2; worker++ {
		go func(seed int64) {
			rng := rand.New(rand.NewSource(seed))
			best := result{score: 1 << 30}
			for restart := 0; restart < 4; restart++ {
				order := rng.Perm(n)
				score := 0
				for i := 1; i < n; i++ {
					score += distance[order[i-1]][order[i]]
				}
				for iteration := 0; iteration < 25000; iteration++ {
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
						if score < best.score {
							best = result{slices.Clone(order), score}
						}
					}
				}
			}
			done <- best
		}(int64(74 + worker))
	}
	a, b := <-done, <-done
	if b.score < a.score || b.score == a.score && slices.Compare(b.order, a.order) < 0 {
		a = b
	}
	return a.order
}

func main() {
	workers := min(2, runtime.GOMAXPROCS(0))
	runtime.GOMAXPROCS(workers)
	in := bufio.NewReader(os.Stdin)
	out := bufio.NewWriterSize(os.Stdout, 1<<20)
	var n, k, p, r int
	fmt.Fscan(in, &n, &k, &p, &r)
	patterns := make([]uint64, p)
	targets := make([]Target, p)
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
	permutation := design(patterns, n)
	for i, bits := range patterns {
		var reordered uint64
		for j, original := range permutation {
			reordered |= (bits >> original & 1) << j
		}
		targets[i] = newTarget(reordered, n)
	}
	for paper := 0; paper < k; paper++ {
		s := make([]byte, n)
		for j := range s {
			s[j] = '.'
		}
		if paper <= n {
			for j := 0; j < min(paper+1, n); j++ {
				s[permutation[j]] = '1'
			}
			if paper < n {
				s[permutation[paper]] = '0'
			}
		}
		fmt.Fprintln(out, string(s))
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
	spent := time.Duration(0)
	for turn := 0; turn < r; turn++ {
		var request int
		if _, err := fmt.Fscan(in, &request); err != nil || request == -1 {
			return
		}
		begin := time.Now()
		cpu := cpuTime()
		quota := max(time.Duration(0), (1400*time.Millisecond-max(spent, cpu))/time.Duration(r-turn))
		deadline, cpuDeadline := begin.Add(quota), cpu+quota
		choice := solve(order, &targets[request])
		candidates := make([]Candidate, 0, 4)
		for mode := 0; mode < 4; mode++ {
			c, ok := build(order, &targets[request], choice, mode)
			duplicate := false
			for _, old := range candidates {
				duplicate = duplicate || slices.Equal(c.order, old.order)
			}
			if ok && !duplicate {
				candidates = append(candidates, c)
			}
		}
		if len(candidates) == 0 {
			candidates = append(candidates, fallback(order, &targets[request]))
		}
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
		best, weight := 0, max(1, samples)
		for i := 1; i < len(candidates); i++ {
			a, b := &candidates[i], &candidates[best]
			sa, sb := len(a.moves)*weight+a.sum, len(b.moves)*weight+b.sum
			if sa < sb || sa == sb && (len(a.moves) < len(b.moves) ||
				len(a.moves) == len(b.moves) && slices.Compare(a.order, b.order) < 0) {
				best = i
			}
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
