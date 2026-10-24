package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strconv"

	// "github.com/emirpasic/gods/queues/priorityqueue"
	"container/list"
)

func main() {
	fs := NewFastScanner(os.Stdin)
	out := bufio.NewWriterSize(os.Stdout, 1<<20)
	defer out.Flush()

	N, M, S, T := fs.NextInt(), fs.NextInt(), fs.NextInt(), fs.NextInt()

	minNext := make([]int, N+1)
	for i := 0; i <= N; i++ {
		minNext[i] = N + 1
	}

	GRAPH := make([][]int, N+1)
	for i := 0; i < M; i++ {
		A, B := fs.NextInt(), fs.NextInt()
		GRAPH[A] = append(GRAPH[A], B)
		if B < minNext[A] {
			minNext[A] = B
		}
	}

	dist := make([]int, N+1)
	for i := 0; i <= N; i++ {
		dist[i] = -1
	}
	dist[S] = 0

	type State struct {
		v, cost int
	}

	deque := list.New()
	deque.PushBack(State{S, 0})

	for deque.Len() > 0 {
		head := deque.Front()
		current := head.Value.(State)
		deque.Remove(head)

		if current.cost != dist[current.v] {
			continue
		}

		for _, next := range GRAPH[current.v] {
			cost := 1
			if next == minNext[current.v] {
				cost = 0
			}

			newCost := current.cost + cost
			if dist[next] != -1 && dist[next] <= newCost {
				continue
			}

			dist[next] = newCost
			if cost == 0 {
				deque.PushFront(State{next, newCost})
			} else {
				deque.PushBack(State{next, newCost})
			}
		}
	}
	fmt.Fprintln(out, dist[T])
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
