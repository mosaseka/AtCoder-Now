package main

import (
	"bufio"
	"fmt"
	"math/rand"
	"os"
	"slices"
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

type DP struct {
	base   int
	table  [2][]Choice
	active [2][]int
}

func newDP(n int) *DP {
	d := &DP{base: n + 1}
	for b := 0; b < 2; b++ {
		d.table[b] = make([]Choice, d.base*d.base)
		d.active[b] = make([]int, 0, len(d.table[b]))
		for i := range d.table[b] {
			d.table[b][i].cost = 255
		}
	}
	return d
}

func (d *DP) relax(buffer, index int, value Choice) {
	old := &d.table[buffer][index]
	if better(value, *old) {
		if old.cost == 255 {
			d.active[buffer] = append(d.active[buffer], index)
		}
		*old = value
	}
}

func (d *DP) solve(order []int, t *Target) Choice {
	for b := 0; b < 2; b++ {
		for _, index := range d.active[b] {
			d.table[b][index].cost = 255
		}
		d.active[b] = d.active[b][:0]
	}
	d.table[0][0] = Choice{}
	d.active[0] = append(d.active[0], 0)
	current, next := 0, 1
	n := len(order) - 1
	for _, k := range order {
		for _, index := range d.active[next] {
			d.table[next][index].cost = 255
		}
		d.active[next] = d.active[next][:0]
		strength, level := min(k, n-1)+1, t.level[k]+1
		for _, index := range d.active[current] {
			maximum, barrier := index/d.base, index%d.base
			value := d.table[current][index]
			// A moved paper must not remain hidden behind a retained paper.
			if strength > maximum {
				moved := value
				moved.cost++
				if k == n {
					moved.last = true
				} else {
					moved.moved |= uint64(1) << k
				}
				d.relax(next, index, moved)
			}
			if !t.core[k] || level > barrier {
				d.relax(next, max(maximum, strength)*d.base+max(barrier, level), value)
			}
		}
		current, next = next, current
	}
	best := Choice{cost: 255}
	for _, index := range d.active[current] {
		if value := d.table[current][index]; better(value, best) {
			best = value
		}
	}
	return best
}

type Move struct{ paper, depth int }
type Candidate struct {
	order []int
	moves []Move
	sum   int
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

func main() {
	in := bufio.NewReader(os.Stdin)
	out := bufio.NewWriterSize(os.Stdout, 1<<20)
	var n, k, p, r int
	fmt.Fscan(in, &n, &k, &p, &r)
	targets := make([]Target, p)
	for i := range targets {
		var s string
		fmt.Fscan(in, &s)
		var bits uint64
		for j := range s {
			if s[j] == '1' {
				bits |= uint64(1) << j
			}
		}
		targets[i] = newTarget(bits, n)
	}
	for paper := 0; paper < k; paper++ {
		s := make([]byte, n)
		for j := range s {
			s[j] = '.'
		}
		if paper <= n {
			for j := 0; j < min(paper+1, n); j++ {
				s[j] = '1'
			}
			if paper < n {
				s[paper] = '0'
			}
		}
		fmt.Fprintln(out, string(s))
	}
	out.Flush()
	order := make([]int, n+1)
	for i := range order {
		order[i] = i
	}
	dp := newDP(n)
	rng := rand.New(rand.NewSource(74))
	spent := time.Duration(0)
	for turn := 0; turn < r; turn++ {
		var request int
		if _, err := fmt.Fscan(in, &request); err != nil || request == -1 {
			return
		}
		begin := time.Now()
		deadline := begin.Add(max(time.Duration(0), (1300*time.Millisecond-spent)/time.Duration(r-turn)))
		choice := dp.solve(order, &targets[request])
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
			for _, next := range rng.Perm(p) {
				if next == request {
					continue
				}
				if samples == 64 || !time.Now().Before(deadline) {
					break
				}
				for i := range candidates {
					candidates[i].sum += int(dp.solve(candidates[i].order, &targets[next]).cost)
				}
				samples++
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
