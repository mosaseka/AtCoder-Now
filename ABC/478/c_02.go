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

	N, K := fs.NextInt(), fs.NextInt()

	A_LIST := make([]int64, N)
	for i := 0; i < N; i++ {
		A_LIST[i] = fs.NextInt64()
	}

	leftBad, rightBad := N, -1
	for i := 0; i+1 < N; i++ {
		if A_LIST[i] > A_LIST[i+1] {
			leftBad = min(leftBad, i)
			rightBad = max(rightBad, i)
		}
	}

	if rightBad == -1 {
		fmt.Fprintln(out, "Yes")
		return
	}

	windowMin := make([]int64, N-K+1)
	windowMax := make([]int64, N-K+1)
	minDeque := make([]int, 0, N)
	maxDeque := make([]int, 0, N)

	for i := 0; i < N; i++ {
		for len(minDeque) > 0 && minDeque[0] <= i-K {
			minDeque = minDeque[1:]
		}
		for len(maxDeque) > 0 && maxDeque[0] <= i-K {
			maxDeque = maxDeque[1:]
		}
		for len(minDeque) > 0 && A_LIST[minDeque[len(minDeque)-1]] >= A_LIST[i] {
			minDeque = minDeque[:len(minDeque)-1]
		}
		for len(maxDeque) > 0 && A_LIST[maxDeque[len(maxDeque)-1]] <= A_LIST[i] {
			maxDeque = maxDeque[:len(maxDeque)-1]
		}
		minDeque = append(minDeque, i)
		maxDeque = append(maxDeque, i)

		if i >= K-1 {
			l := i - K + 1
			windowMin[l] = A_LIST[minDeque[0]]
			windowMax[l] = A_LIST[maxDeque[0]]
		}
	}

	start := max(0, rightBad-K+1)
	end := min(leftBad, N-K)
	for l := start; l <= end; l++ {
		r := l + K - 1
		if l > 0 && A_LIST[l-1] > windowMin[l] {
			continue
		}
		if r+1 < N && windowMax[l] > A_LIST[r+1] {
			continue
		}
		fmt.Fprintln(out, "Yes")
		return
	}
	fmt.Fprintln(out, "No")
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
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
