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

// Bの先頭x個の和
func PrefixSum(x int64, P, C []int64) int64 {
	// m(m+1)/2 <= x を満たす最大の整数を、解の公式に従って求める平方根の公式で求める。
	m := int64((math.Sqrt(float64(1+8*x)) - 1) / 2)
	r := x - m*(m+1)/2
	return C[m] + P[r]
}

func main() {
	fs := NewFastScanner(os.Stdin)
	out := bufio.NewWriterSize(os.Stdout, 1<<20)
	defer out.Flush()

	N, Q := fs.NextInt(), fs.NextInt()

	// P[i]: Aの先頭i個の和
	// C[i]: Bの最初のiブロックの和
	P := make([]int64, N+1)
	C := make([]int64, N+1)
	for i := 1; i <= N; i++ {
		P[i] = P[i-1] + fs.NextInt64()
		C[i] = C[i-1] + P[i]
	}

	for i := 0; i < Q; i++ {
		L, R := fs.NextInt64(), fs.NextInt64()
		fmt.Fprintln(out, PrefixSum(R, P, C)-PrefixSum(L-1, P, C))
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
