package main

import (
	"bufio"
	"bytes"
	"io"
	"math/bits"
	"os"
	"strconv"
	"time"

	"github.com/emirpasic/gods/queues/priorityqueue"
)

const (
	bestFirstMillis = 1250
	hillMillis      = 1700
	macroMillis     = 120
)

type Point struct {
	i int
	j int
}

type DeliveryKey struct {
	pos int
	dir int
	k   int
}

type Delivery struct {
	ops []byte
	pos int
	dir int
}

type Solution struct {
	delivered int
	ops       []byte
	order     []int
}

type State struct {
	length int
	bits   uint64
	pos    int
	dir    int
	order  []int
}

type Candidate struct {
	rank   int
	length int
	bits   uint64
	pos    int
	dir    int
	order  []int
}

type SeenKey struct {
	bits uint64
	pos  int
	dir  int
}

var (
	startTime     time.Time
	n, m, t       int
	v, h          []string
	balls         []int
	baskets       []int
	cellCount     int
	pathCache     map[int][]int
	deliveryCache map[DeliveryKey]Delivery
	di            = []int{0, 1, 0, -1}
	dj            = []int{1, 0, -1, 0}
)

func main() {
	startTime = time.Now()
	fs := NewFastScanner(os.Stdin)
	out := bufio.NewWriterSize(os.Stdout, 1<<20)
	defer out.Flush()

	n = fs.NextInt()
	m = fs.NextInt()
	t = fs.NextInt()
	cellCount = n * n

	v = make([]string, n)
	for i := 0; i < n; i++ {
		v[i] = fs.Next()
	}
	h = make([]string, n-1)
	for i := 0; i < n-1; i++ {
		h[i] = fs.Next()
	}

	balls = make([]int, m)
	baskets = make([]int, m)
	for k := 0; k < m; k++ {
		b := fs.NextInt()
		c := fs.NextInt()
		d := fs.NextInt()
		e := fs.NextInt()
		balls[k] = encode(b, c)
		baskets[k] = encode(d, e)
	}

	pathCache = make(map[int][]int)
	deliveryCache = make(map[DeliveryKey]Delivery)

	best := solveBase()

	cand := solveBestFirst(best)
	if better(cand, best) {
		best = cand
	}

	cand = solveHillClimb(best)
	if better(cand, best) {
		best = cand
	}

	answer := best.ops
	if best.delivered == m {
		answer = compressMacro(answer)
	}

	for _, op := range answer {
		out.WriteByte(op)
		out.WriteByte('\n')
	}
}

func encode(i, j int) int {
	return i*n + j
}

func canMove(pos, dir int) bool {
	i := pos / n
	j := pos % n
	switch dir {
	case 0:
		return j+1 < n && v[i][j] == '0'
	case 1:
		return i+1 < n && h[i][j] == '0'
	case 2:
		return j-1 >= 0 && v[i][j-1] == '0'
	default:
		return i-1 >= 0 && h[i-1][j] == '0'
	}
}

func bfs(start, goal int) []int {
	if start == goal {
		return []int{}
	}

	prevPos := make([]int, cellCount)
	prevDir := make([]int, cellCount)
	for i := 0; i < cellCount; i++ {
		prevPos[i] = -1
		prevDir[i] = -1
	}

	queue := make([]int, 0, cellCount)
	queue = append(queue, start)
	prevPos[start] = start

	found := false
	for head := 0; head < len(queue) && !found; head++ {
		pos := queue[head]
		i := pos / n
		j := pos % n
		for nd := 0; nd < 4; nd++ {
			if !canMove(pos, nd) {
				continue
			}
			ni := i + di[nd]
			nj := j + dj[nd]
			next := encode(ni, nj)
			if prevPos[next] != -1 {
				continue
			}
			prevPos[next] = pos
			prevDir[next] = nd
			if next == goal {
				found = true
				break
			}
			queue = append(queue, next)
		}
	}

	path := make([]int, 0, cellCount)
	for cur := goal; cur != start; cur = prevPos[cur] {
		path = append(path, prevDir[cur])
	}
	reverseInts(path)
	return path
}

func getPath(start, goal int) []int {
	key := start*cellCount + goal
	if path, ok := pathCache[key]; ok {
		return path
	}
	path := bfs(start, goal)
	pathCache[key] = path
	return path
}

func route(pos, dir, goal int) ([]byte, int, int) {
	path := getPath(pos, goal)
	ops := make([]byte, 0, len(path)*3)
	d := dir
	for _, nd := range path {
		diff := (nd - d + 4) % 4
		switch diff {
		case 1:
			ops = append(ops, 'R')
		case 2:
			ops = append(ops, 'R', 'R')
		case 3:
			ops = append(ops, 'L')
		}
		ops = append(ops, 'F')
		d = nd
	}
	return ops, goal, d
}

func delivery(pos, dir, k int) Delivery {
	key := DeliveryKey{pos: pos, dir: dir, k: k}
	if res, ok := deliveryCache[key]; ok {
		return res
	}

	ops1, pos1, dir1 := route(pos, dir, balls[k])
	ops2, pos2, dir2 := route(pos1, dir1, baskets[k])
	ops := make([]byte, 0, len(ops1)+len(ops2)+2)
	ops = append(ops, ops1...)
	ops = append(ops, 'S')
	ops = append(ops, ops2...)
	ops = append(ops, 'S')

	res := Delivery{ops: ops, pos: pos2, dir: dir2}
	deliveryCache[key] = res
	return res
}

func better(a, b Solution) bool {
	if a.delivered != b.delivered {
		return a.delivered > b.delivered
	}
	return len(a.ops) < len(b.ops)
}

func completeGreedy(pos, dir int, used []bool, answer []byte, order []int) Solution {
	for {
		bestK := -1
		var bestDelivery Delivery

		for k := 0; k < m; k++ {
			if used[k] {
				continue
			}
			d := delivery(pos, dir, k)
			if len(answer)+len(d.ops) > t {
				continue
			}
			if bestK == -1 || len(d.ops) < len(bestDelivery.ops) {
				bestK = k
				bestDelivery = d
			}
		}

		if bestK == -1 {
			break
		}

		answer = append(answer, bestDelivery.ops...)
		order = append(order, bestK)
		used[bestK] = true
		pos = bestDelivery.pos
		dir = bestDelivery.dir
	}

	return Solution{
		delivered: len(order),
		ops:       append([]byte(nil), answer...),
		order:     append([]int(nil), order...),
	}
}

func solveBase() Solution {
	used := make([]bool, m)
	return completeGreedy(0, 0, used, []byte{}, []int{})
}

func solveWithPrefix(prefix []int) Solution {
	pos := 0
	dir := 0
	used := make([]bool, m)
	answer := make([]byte, 0, t)
	order := make([]int, 0, m)

	for _, k := range prefix {
		if used[k] {
			continue
		}
		d := delivery(pos, dir, k)
		if len(answer)+len(d.ops) > t {
			break
		}
		answer = append(answer, d.ops...)
		order = append(order, k)
		used[k] = true
		pos = d.pos
		dir = d.dir
	}

	return completeGreedy(pos, dir, used, answer, order)
}

func solveByPriority(priority []int) Solution {
	pos := 0
	dir := 0
	used := make([]bool, m)
	answer := make([]byte, 0, t)
	order := make([]int, 0, m)

	for _, k := range priority {
		if used[k] {
			continue
		}
		d := delivery(pos, dir, k)
		if len(answer)+len(d.ops) <= t {
			answer = append(answer, d.ops...)
			order = append(order, k)
			used[k] = true
			pos = d.pos
			dir = d.dir
		}
	}

	return completeGreedy(pos, dir, used, answer, order)
}

func stateEstimate(pos, dir int, usedBits uint64) int {
	best := 1 << 60
	for k := 0; k < m; k++ {
		if (usedBits>>uint(k))&1 != 0 {
			continue
		}
		d := delivery(pos, dir, k)
		if len(d.ops) < best {
			best = len(d.ops)
		}
	}
	if best == 1<<60 {
		return 0
	}
	return best
}

func solveBestFirst(base Solution) Solution {
	deadline := startTime.Add(bestFirstMillis * time.Millisecond)
	width := 420
	if m > 25 {
		width = 300
	}
	evalWidth := 45
	if m > 30 {
		evalWidth = 32
	}

	states := []State{{length: 0, bits: 0, pos: 0, dir: 0, order: []int{}}}
	bestSol := base

	for len(states) > 0 && time.Now().Before(deadline) {
		queue := priorityqueue.NewWith(candidateComparator)

		for _, state := range states {
			if !time.Now().Before(deadline) {
				break
			}
			for k := 0; k < m; k++ {
				if (state.bits>>uint(k))&1 != 0 {
					continue
				}
				d := delivery(state.pos, state.dir, k)
				newLength := state.length + len(d.ops)
				if newLength > t {
					continue
				}
				newBits := state.bits | (uint64(1) << uint(k))
				rank := newLength + stateEstimate(d.pos, d.dir, newBits)/3
				queue.Enqueue(Candidate{
					rank:   rank,
					length: newLength,
					bits:   newBits,
					pos:    d.pos,
					dir:    d.dir,
					order:  appendOrder(state.order, k),
				})
			}
		}

		if queue.Empty() {
			break
		}

		states = make([]State, 0, width)
		seen := make(map[SeenKey]bool, width*2)

		for !queue.Empty() && len(states) < width {
			value, ok := queue.Dequeue()
			if !ok {
				break
			}
			cand := value.(Candidate)
			key := SeenKey{bits: cand.bits, pos: cand.pos, dir: cand.dir}
			if seen[key] {
				continue
			}
			seen[key] = true
			states = append(states, State{
				length: cand.length,
				bits:   cand.bits,
				pos:    cand.pos,
				dir:    cand.dir,
				order:  cand.order,
			})
		}

		limit := evalWidth
		if len(states) < limit {
			limit = len(states)
		}
		for i := 0; i < limit; i++ {
			if !time.Now().Before(deadline) {
				break
			}
			sol := solveWithPrefix(states[i].order)
			if better(sol, bestSol) {
				bestSol = sol
			}
		}
	}

	return bestSol
}

func candidateComparator(a, b interface{}) int {
	x := a.(Candidate)
	y := b.(Candidate)
	if x.rank != y.rank {
		return x.rank - y.rank
	}
	if x.length != y.length {
		return x.length - y.length
	}
	xc := bits.OnesCount64(x.bits)
	yc := bits.OnesCount64(y.bits)
	if xc != yc {
		return yc - xc
	}
	if x.pos != y.pos {
		return x.pos - y.pos
	}
	return x.dir - y.dir
}

func solveHillClimb(base Solution) Solution {
	deadline := startTime.Add(hillMillis * time.Millisecond)
	used := make([]bool, m)
	priority := make([]int, 0, m)
	for _, k := range base.order {
		if !used[k] {
			used[k] = true
			priority = append(priority, k)
		}
	}
	for k := 0; k < m; k++ {
		if !used[k] {
			priority = append(priority, k)
		}
	}

	current := solveByPriority(priority)
	if better(base, current) {
		current = base
	}

	improved := true
	for improved && time.Now().Before(deadline) {
		improved = false

		for i := 0; i < m && time.Now().Before(deadline); i++ {
			for j := 0; j < m; j++ {
				if i == j {
					continue
				}
				candOrder := make([]int, len(priority))
				copy(candOrder, priority)
				x := candOrder[i]
				if i < j {
					copy(candOrder[i:j], candOrder[i+1:j+1])
					candOrder[j] = x
				} else {
					copy(candOrder[j+1:i+1], candOrder[j:i])
					candOrder[j] = x
				}

				cand := solveByPriority(candOrder)
				if better(cand, current) {
					priority = candOrder
					current = cand
					improved = true
					break
				}
			}
			if improved {
				break
			}
		}
	}

	return current
}

func expandMacro(ops []byte) []byte {
	lastMacro := []byte{}
	recording := false
	recordingMacro := []byte{}
	expanded := []byte{}

	for _, op := range ops {
		switch op {
		case 'F', 'R', 'L', 'S':
			expanded = append(expanded, op)
			if recording {
				recordingMacro = append(recordingMacro, op)
			}
		case 'M':
			if recording {
				lastMacro = append([]byte(nil), recordingMacro...)
				recording = false
			} else {
				recordingMacro = []byte{}
				recording = true
			}
		case 'P':
			if len(lastMacro) > 0 {
				expanded = append(expanded, lastMacro...)
				if recording {
					recordingMacro = append(recordingMacro, lastMacro...)
				}
			}
		}
	}

	return expanded
}

func buildMacroOutput(basic, macro string, positions []int) []byte {
	length := len(macro)
	use := make(map[int]bool, len(positions))
	for _, pos := range positions {
		use[pos] = true
	}

	output := make([]byte, 0, len(basic))
	first := true
	for i := 0; i < len(basic); {
		if use[i] {
			if first {
				output = append(output, 'M')
				output = append(output, macro...)
				output = append(output, 'M')
				first = false
			} else {
				output = append(output, 'P')
			}
			i += length
		} else {
			output = append(output, basic[i])
			i++
		}
	}

	return output
}

func compressMacro(answer []byte) []byte {
	basic := string(answer)
	size := len(basic)
	if size < 4 {
		return answer
	}

	deadline := time.Now().Add(macroMillis * time.Millisecond)
	maxLen := 80
	if size < maxLen {
		maxLen = size
	}

	bestGain := 0
	bestHasS := 0
	bestHasTurn := 0
	bestLen := 0
	bestMacro := ""
	var bestPositions []int

	for length := 2; length <= maxLen; length++ {
		expired := false
		positions := make(map[string][]int, size-length+1)

		limit := size - length + 1
		for i := 0; i < limit; i++ {
			if (i&2047) == 0 && !time.Now().Before(deadline) {
				expired = true
				break
			}
			macro := basic[i : i+length]
			positions[macro] = append(positions[macro], i)
		}

		idx := 0
		for macro, posList := range positions {
			if (idx&4095) == 0 && !time.Now().Before(deadline) {
				expired = true
				break
			}
			idx++
			if len(posList) < 2 {
				continue
			}

			selected := make([]int, 0, len(posList))
			last := -length
			for _, pos := range posList {
				if last+length <= pos {
					selected = append(selected, pos)
					last = pos
				}
			}

			count := len(selected)
			if count < 2 {
				continue
			}

			gain := (count-1)*(length-1) - 2
			if gain <= 0 {
				continue
			}

			hasS := 0
			if bytes.IndexByte([]byte(macro), 'S') >= 0 {
				hasS = 1
			}
			hasTurn := 0
			if bytes.IndexByte([]byte(macro), 'L') >= 0 || bytes.IndexByte([]byte(macro), 'R') >= 0 {
				hasTurn = 1
			}

			if macroScoreBetter(gain, hasS, hasTurn, length, bestGain, bestHasS, bestHasTurn, bestLen) {
				bestGain = gain
				bestHasS = hasS
				bestHasTurn = hasTurn
				bestLen = length
				bestMacro = macro
				bestPositions = selected
			}
		}

		if expired {
			break
		}
	}

	if bestMacro == "" {
		return answer
	}

	output := buildMacroOutput(basic, bestMacro, bestPositions)
	if len(output) < size && bytes.Equal(expandMacro(output), answer) {
		return output
	}

	return answer
}

func macroScoreBetter(gain, hasS, hasTurn, length, bestGain, bestHasS, bestHasTurn, bestLen int) bool {
	if gain != bestGain {
		return gain > bestGain
	}
	if hasS != bestHasS {
		return hasS > bestHasS
	}
	if hasTurn != bestHasTurn {
		return hasTurn > bestHasTurn
	}
	return length > bestLen
}

func appendOrder(order []int, k int) []int {
	next := make([]int, len(order)+1)
	copy(next, order)
	next[len(order)] = k
	return next
}

func reverseInts(a []int) {
	for l, r := 0, len(a)-1; l < r; l, r = l+1, r-1 {
		a[l], a[r] = a[r], a[l]
	}
}

type FastScanner struct {
	in     io.Reader
	buffer []byte
	ptr    int
	buflen int
}

func NewFastScanner(r io.Reader) *FastScanner {
	return &FastScanner{
		in:     r,
		buffer: make([]byte, 1<<16),
	}
}

func (fs *FastScanner) hasNextByte() bool {
	if fs.ptr < fs.buflen {
		return true
	}
	fs.ptr = 0
	n, err := fs.in.Read(fs.buffer)
	if err != nil {
		return false
	}
	fs.buflen = n
	return fs.buflen > 0
}

func (fs *FastScanner) readByte() int {
	if fs.hasNextByte() {
		b := fs.buffer[fs.ptr]
		fs.ptr++
		return int(b)
	}
	return -1
}

func isPrintableChar(c int) bool {
	return 33 <= c && c <= 126
}

func (fs *FastScanner) HasNext() bool {
	for fs.hasNextByte() && !isPrintableChar(int(fs.buffer[fs.ptr])) {
		fs.ptr++
	}
	return fs.hasNextByte()
}

func (fs *FastScanner) Next() string {
	if !fs.HasNext() {
		panic("NoSuchElementException")
	}
	b := make([]byte, 0, 16)
	c := fs.readByte()
	for isPrintableChar(c) {
		b = append(b, byte(c))
		c = fs.readByte()
	}
	return string(b)
}

func (fs *FastScanner) NextInt64() int64 {
	if !fs.HasNext() {
		panic("NoSuchElementException")
	}

	var num int64
	minus := false

	b := fs.readByte()
	if b == '-' {
		minus = true
		b = fs.readByte()
	}
	if b < '0' || '9' < b {
		panic("NumberFormatException")
	}

	for {
		if '0' <= b && b <= '9' {
			num = num*10 + int64(b-'0')
		} else if b == -1 || !isPrintableChar(b) {
			if minus {
				return -num
			}
			return num
		} else {
			panic("NumberFormatException")
		}
		b = fs.readByte()
	}
}

func (fs *FastScanner) NextInt() int {
	x := fs.NextInt64()
	if x < -2147483648 || x > 2147483647 {
		panic("NumberFormatException")
	}
	return int(x)
}

func (fs *FastScanner) NextFloat64() float64 {
	s := fs.Next()
	v, err := strconv.ParseFloat(s, 64)
	if err != nil {
		panic("NumberFormatException")
	}
	return v
}
