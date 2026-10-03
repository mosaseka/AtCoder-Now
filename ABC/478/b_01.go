package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strconv"
	// "github.com/emirpasic/gods/queues/priorityqueue"
)

func combinations(list []int, choose, buf int) (c chan []int) {
	c = make(chan []int, buf)
	go func() {
		defer close(c)
		switch {
		case choose == 0:
			c <- []int{}
		case choose == len(list):
			c <- list
		case len(list) < choose:
			return
		default:
			for i := 0; i < len(list); i++ {
				for subComb := range combinations(list[i+1:], choose-1, buf) {
					c <- append([]int{list[i]}, subComb...)
				}
			}
		}
	}()
	return
}

func main() {
	fs := NewFastScanner(os.Stdin)
	out := bufio.NewWriterSize(os.Stdout, 1<<20)
	defer out.Flush()

	N, V := fs.NextInt(), fs.NextInt()

	W_LIST := make([][2]int, N)
	for i := 0; i < N; i++ {
		W_LIST[i] = [2]int{fs.NextInt(), i + 1}
	}

	MAX := 0
	for comb := range combinations(W_LIST, 3, 100) {
		if comb[0][1]+comb[1][1]+comb[2][1] <= V {
			MAX = max(MAX, sum([]int{comb[0][0], comb[1][0], comb[2][0]}))
		}
	}
	fmt.Fprintln(out, MAX)
}

func sum(list []int) int {
	SUM := 0
	for _, v := range list {
		SUM += v
	}
	return SUM
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
