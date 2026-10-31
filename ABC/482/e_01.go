package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strconv"

	"github.com/emirpasic/gods/queues/linkedlistqueue"
)

func BFS(graph [][]int, start int) (int, []int, []int) {
	N := len(graph)
	dist := make([]int, N)
	parent := make([]int, N)
	for i := 0; i < N; i++ {
		dist[i] = -1
		parent[i] = -1
	}

	queue := linkedlistqueue.New()
	queue.Enqueue(start)
	dist[start] = 0
	max := start

	for !queue.Empty() {
		value, _ := queue.Dequeue()
		vertex := value.(int)

		if dist[vertex] > dist[max] {
			max = vertex
		}

		for _, next := range graph[vertex] {
			if dist[next] != -1 {
				continue
			}
			dist[next] = dist[vertex] + 1
			parent[next] = vertex
			queue.Enqueue(next)
		}
	}
	return max, dist, parent
}

func collectColors(graph [][]int, colors []int, start, blocked, target int) []int {
	type state struct {
		v, parent, depth int
	}

	stack := []state{{start, blocked, 0}}
	result := make([]int, 0)

	for len(stack) > 0 {
		s := stack[len(stack)-1]
		stack = stack[0 : len(stack)-1]

		if s.depth == target {
			result = append(result, colors[s.v])
			continue
		}

		for _, next := range graph[s.v] {
			if next == s.parent {
				continue
			}
			stack = append(stack, state{next, s.v, s.depth + 1})
		}
	}
	return result
}

func main() {
	fs := NewFastScanner(os.Stdin)
	out := bufio.NewWriterSize(os.Stdout, 1<<20)
	defer out.Flush()

	N := fs.NextInt()

	GRAPH := make([][]int, N)

	for i := 0; i < N-1; i++ {
		u, v := fs.NextInt(), fs.NextInt()
		GRAPH[u-1] = append(GRAPH[u-1], v-1)
		GRAPH[v-1] = append(GRAPH[v-1], u-1)
	}

	C_LIST := make([]int, N)
	for i := 0; i < N; i++ {
		C_LIST[i] = fs.NextInt()
	}

	a, _, _ := BFS(GRAPH, 0)
	b, dist, parent := BFS(GRAPH, a)
	D := dist[b]

	path := make([]int, 0, D+1)
	for v := b; v != -1; v = parent[v] {
		path = append(path, v)
	}

	r := D / 2
	seen := make([]int, N+1)
	answer := 0

	if D%2 == 1 {
		left, right := path[r], path[r+1]

		for _, color := range collectColors(GRAPH, C_LIST, left, right, r) {
			seen[color]++
		}

		for _, color := range collectColors(GRAPH, C_LIST, right, left, r) {
			answer += seen[color]
		}
	} else {
		center := path[r]

		for _, next := range GRAPH[center] {
			batch := collectColors(GRAPH, C_LIST, next, center, r-1)
			for _, color := range batch {
				answer += seen[color]
			}
			for _, color := range batch {
				seen[color]++
			}
		}
	}
	fmt.Fprintln(out, answer)
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
