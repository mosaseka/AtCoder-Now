package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strconv"
	// "github.com/emirpasic/gods/queues/priorityqueue"
)

func main() {
	fs := NewFastScanner(os.Stdin)
	out := bufio.NewWriterSize(os.Stdout, 1<<20)
	defer out.Flush()

	const MOD int = 998244353

	N, M := fs.NextInt(), fs.NextInt()

	type egde struct {
		to, digit int
	}

	graph := make([][]egde, N+1)
	for i := 0; i < M; i++ {
		A, B, C := fs.NextInt(), fs.NextInt(), fs.NextInt()
		graph[A] = append(graph[A], egde{B, C})
	}

	visited := make([]bool, N+1)
	answer := make([]int, N+1)
	visited[1] = true

	groups := [][]int{{1}}

	for i := 0; i < len(groups); i++ {
		group := groups[i]
		base := answer[group[0]]

		var check [10][]int
		for _, v := range group {
			for _, e := range graph[v] {
				if !visited[e.to] {
					check[e.digit] = append(check[e.digit], e.to)
				}
			}
		}

		for digit := 1; digit <= 9; digit++ {
			var nextGroup []int
			for _, next := range check[digit] {
				if visited[next] {
					continue
				}

				visited[next] = true
				answer[next] = (base*10 + digit) % MOD
				nextGroup = append(nextGroup, next)
			}

			if len(nextGroup) > 0 {
				groups = append(groups, nextGroup)
			}
		}
	}
	for i := 2; i <= N; i++ {
		fmt.Fprintln(out, answer[i])
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
