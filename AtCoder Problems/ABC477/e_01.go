package main

import (
	"bufio"
	"fmt"
	"github.com/emirpasic/gods/queues/priorityqueue"
	"io"
	"os"
	"strconv"
)

type Edge struct {
	to     int
	weight int64
}

type State struct {
	vertex int
	dist   int64
}

func dijkstra(graph [][]Edge, start int) []int64 {
	const inf int64 = 1 << 60
	dist := make([]int64, len(graph))
	for i := range dist {
		dist[i] = inf
	}
	dist[start] = 0

	pq := priorityqueue.NewWith(func(a, b interface{}) int {
		x, y := a.(State), b.(State)
		if x.dist < y.dist {
			return -1
		}
		if x.dist > y.dist {
			return 1
		}
		return 0
	})
	pq.Enqueue(State{vertex: start, dist: 0})
	for !pq.Empty() {
		value, _ := pq.Dequeue()
		current := value.(State)
		// より短い距離が見つかった後の、古い登録は処理しない。
		if current.dist != dist[current.vertex] {
			continue
		}
		for _, edge := range graph[current.vertex] {
			nextDist := current.dist + edge.weight
			if nextDist < dist[edge.to] {
				dist[edge.to] = nextDist
				pq.Enqueue(State{vertex: edge.to, dist: nextDist})
			}
		}
	}
	return dist
}

func main() {
	fs := NewFastScanner(os.Stdin)
	out := bufio.NewWriterSize(os.Stdout, 1<<20)
	defer out.Flush()

	N, Q := fs.NextInt(), fs.NextInt()

	// 0 始まりで、環の頂点は 0〜N-1、中心の頂点は N。
	graph := make([][]Edge, N+1)
	prefix := make([]int64, N+1)
	for i := 0; i < N; i++ {
		a := fs.NextInt64()
		prefix[i+1] = prefix[i] + a
		j := (i + 1) % N
		graph[i] = append(graph[i], Edge{to: j, weight: a})
		graph[j] = append(graph[j], Edge{to: i, weight: a})
	}

	for i := 0; i < N; i++ {
		b := fs.NextInt64()
		graph[i] = append(graph[i], Edge{to: N, weight: b})
		graph[N] = append(graph[N], Edge{to: i, weight: b})
	}

	dist := dijkstra(graph, N)
	for i := 0; i < Q; i++ {
		s, t := fs.NextInt()-1, fs.NextInt()-1
		answer := dist[s] + dist[t]
		if s != N && t != N {
			if s > t {
				s, t = t, s
			}
			clockwise := prefix[t] - prefix[s]
			counterclockwise := prefix[N] - clockwise
			if clockwise < answer {
				answer = clockwise
			}
			if counterclockwise < answer {
				answer = counterclockwise
			}
		}
		fmt.Fprintln(out, answer)
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
