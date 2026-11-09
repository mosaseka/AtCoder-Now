package main

import (
	"bufio"
	"fmt"
	"io"
	"math"
	"os"
	"strconv"
	// "github.com/emirpasic/gods/queues/priorityqueue"
)

func main() {
	fs := NewFastScanner(os.Stdin)
	out := bufio.NewWriterSize(os.Stdout, 1<<20)
	N := fs.NextInt()
	K := fs.NextInt()
	P := fs.NextInt()
	R := fs.NextInt()

	patterns := make([]uint64, P)
	for i := range patterns {
		pattern := fs.Next()
		for j := 0; j < N; j++ {
			if pattern[j] == '1' {
				patterns[i] |= uint64(1) << j
			}
		}
	}

	models := make(map[int]*LayerModel)
	groups := make([]WindowGroup, 0, (N+4)/5)
	sheets := make([][]byte, K)
	for k := range sheets {
		sheets[k] = make([]byte, N)
		for j := range sheets[k] {
			sheets[k][j] = '.'
		}
	}

	used := 0
	for start := 0; start < N; start += 5 {
		width := min(5, N-start)
		model := models[width]
		if model == nil {
			model = NewLayerModel(width)
			models[width] = model
		}
		groups = append(groups, WindowGroup{start: start, firstSheet: used, model: model})
		for k := 0; k < model.sheetCount; k++ {
			for j := 0; j < width; j++ {
				if model.opaque[k]&(1<<j) != 0 {
					sheets[used+k][start+j] = byte('0' + ((model.ones[k] >> j) & 1))
				}
			}
		}
		used += model.sheetCount
	}
	for _, sheet := range sheets {
		fmt.Fprintln(out, string(sheet))
	}
	out.Flush()

	order := make([]int, K)
	positions := make([]int, K)
	for k := range order {
		order[k] = k
		positions[k] = k
	}
	operations := make([]SheetMove, 0, 2*K)
	for i := 0; i < R; i++ {
		request := fs.NextInt()
		if request == -1 {
			return
		}

		target := patterns[request]
		operations = operations[:0]
		for g := range groups {
			group := &groups[g]
			model := group.model
			pattern := int((target >> group.start) & uint64((1<<model.width)-1))
			goal := model.goal[group.state][pattern]
			for group.state != goal {
				action := int(model.firstMove[group.state][goal])
				localSheet, localDepth := action/model.sheetCount, action%model.sheetCount
				next := model.next[group.state][action]
				sheet := group.firstSheet + localSheet
				depth := K - 1
				if localDepth < model.sheetCount-1 {
					// Insert before the next sheet of this group, after removing sheet.
					anchor := group.firstSheet + model.permutations[next][localDepth+1]
					depth = positions[anchor]
					if positions[sheet] < depth {
						depth--
					}
				}
				operations = append(operations, SheetMove{sheet: sheet, depth: depth})
				moveSheet(order, positions, sheet, depth)
				group.state = next
			}
		}
		fmt.Fprintln(out, len(operations))
		for _, operation := range operations {
			fmt.Fprintln(out, operation.sheet, operation.depth)
		}
		out.Flush()
	}
}

type SheetMove struct {
	sheet int
	depth int
}

type WindowGroup struct {
	start      int
	firstSheet int
	state      int
	model      *LayerModel
}

type LocalTransition struct {
	to     int
	action uint8
}

type LayerModel struct {
	width        int
	sheetCount   int
	opaque       []int
	ones         []int
	permutations [][6]int
	display      []int
	next         [][]int
	distance     [][]uint8
	firstMove    [][]uint8
	goal         [][]int
}

func NewLayerModel(width int) *LayerModel {
	m := &LayerModel{
		width:      width,
		sheetCount: width + 1,
		opaque:     make([]int, width+1),
		ones:       make([]int, width+1),
	}
	// For width 5: 0...., 10..., 110.., 1110., 11110, 11111.
	for k := 0; k < width; k++ {
		m.opaque[k] = (1 << (k + 1)) - 1
		m.ones[k] = (1 << k) - 1
	}
	m.opaque[width] = (1 << width) - 1
	m.ones[width] = m.opaque[width]

	var permutation [6]int
	var enumerate func(int, int)
	enumerate = func(depth, used int) {
		if depth == m.sheetCount {
			m.permutations = append(m.permutations, permutation)
			return
		}
		for k := 0; k < m.sheetCount; k++ {
			if used&(1<<k) == 0 {
				permutation[depth] = k
				enumerate(depth+1, used|(1<<k))
			}
		}
	}
	enumerate(0, 0)
	stateCount := len(m.permutations)
	ids := make(map[int]int, stateCount)
	for state, p := range m.permutations {
		ids[m.permutationKey(p)] = state
	}

	m.display = make([]int, stateCount)
	m.next = make([][]int, stateCount)
	edges := make([][]LocalTransition, stateCount)
	for state, p := range m.permutations {
		covered, value := 0, 0
		var visible [6]bool
		for _, k := range p[:m.sheetCount] {
			exposed := m.opaque[k] &^ covered
			visible[k] = exposed != 0
			value |= m.ones[k] & exposed
			covered |= m.opaque[k]
		}
		m.display[state] = value
		m.next[state] = make([]int, m.sheetCount*m.sheetCount)
		for action := range m.next[state] {
			m.next[state][action] = -1
		}
		for from, k := range p[:m.sheetCount] {
			if !visible[k] {
				continue
			}
			for depth := 0; depth < m.sheetCount; depth++ {
				if depth == from {
					continue
				}
				next := p
				copy(next[from:m.sheetCount-1], next[from+1:m.sheetCount])
				copy(next[depth+1:m.sheetCount], next[depth:m.sheetCount-1])
				next[depth] = k
				to := ids[m.permutationKey(next)]
				action := uint8(k*m.sheetCount + depth)
				edges[state] = append(edges[state], LocalTransition{to: to, action: action})
				m.next[state][action] = to
			}
		}
	}

	// Shortest paths use only sheets visible in the current local state.
	m.distance = make([][]uint8, stateCount)
	m.firstMove = make([][]uint8, stateCount)
	queue := make([]int, stateCount)
	for source := 0; source < stateCount; source++ {
		distance := make([]uint8, stateCount)
		first := make([]uint8, stateCount)
		for state := range distance {
			distance[state] = 255
		}
		distance[source] = 0
		queue[0] = source
		head, tail := 0, 1
		for head < tail {
			state := queue[head]
			head++
			for _, edge := range edges[state] {
				if distance[edge.to] != 255 {
					continue
				}
				distance[edge.to] = distance[state] + 1
				first[edge.to] = first[state]
				if state == source {
					first[edge.to] = edge.action
				}
				queue[tail] = edge.to
				tail++
			}
		}
		m.distance[source] = distance
		m.firstMove[source] = first
	}
	m.buildPolicy()
	return m
}

func (m *LayerModel) permutationKey(p [6]int) int {
	key := 0
	for i := 0; i < m.sheetCount; i++ {
		key |= p[i] << (3 * i)
	}
	return key
}

func (m *LayerModel) buildPolicy() {
	stateCount := len(m.permutations)
	patternCount := 1 << m.width
	future := make([]float64, stateCount)
	updated := make([]float64, stateCount)
	best := make([]float64, patternCount)
	// Relative value iteration for independent, uniformly distributed requests.
	for iteration := 0; iteration < 64; iteration++ {
		for state := 0; state < stateCount; state++ {
			for pattern := range best {
				best[pattern] = math.Inf(1)
			}
			for to, pattern := range m.display {
				cost := float64(m.distance[state][to]) + future[to]
				if cost < best[pattern] {
					best[pattern] = cost
				}
			}
			sum := 0.0
			for _, cost := range best {
				sum += cost
			}
			updated[state] = sum / float64(patternCount)
		}
		reference := updated[0]
		change := 0.0
		for state := range updated {
			updated[state] -= reference
			change = math.Max(change, math.Abs(updated[state]-future[state]))
		}
		future, updated = updated, future
		if change <= 1e-9 {
			break
		}
	}

	m.goal = make([][]int, stateCount)
	for state := 0; state < stateCount; state++ {
		m.goal[state] = make([]int, patternCount)
		for pattern := range best {
			best[pattern] = math.Inf(1)
			m.goal[state][pattern] = -1
		}
		for to, pattern := range m.display {
			cost := float64(m.distance[state][to]) + future[to]
			previous := m.goal[state][pattern]
			if cost < best[pattern]-1e-9 ||
				(math.Abs(cost-best[pattern]) <= 1e-9 &&
					(previous == -1 || m.distance[state][to] < m.distance[state][previous] ||
						(m.distance[state][to] == m.distance[state][previous] && to < previous))) {
				best[pattern] = cost
				m.goal[state][pattern] = to
			}
		}
	}
}

func moveSheet(order, positions []int, sheet, depth int) {
	from := positions[sheet]
	if from < depth {
		copy(order[from:depth], order[from+1:depth+1])
	} else {
		copy(order[depth+1:from+1], order[depth:from])
	}
	order[depth] = sheet
	for i := min(from, depth); i <= max(from, depth); i++ {
		positions[order[i]] = i
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

	var n int64 = 0
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
			n = n*10 + int64(b-'0')
		} else if b == -1 || !isPrintableChar(b) {
			if minus {
				return -n
			}
			return n
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
