package main

import (
	"bufio"
	"fmt"
	"io"
	"math/bits"
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

	for k := 0; k < K; k++ {
		sheet := make([]byte, N)
		for j := range sheet {
			sheet[j] = '.'
		}
		if k < 2*N {
			sheet[k/2] = byte('0' + k%2)
		}
		fmt.Fprintln(out, string(sheet))
	}
	out.Flush()

	var current uint64
	for i := 0; i < R; i++ {
		request := fs.NextInt()
		if request == -1 {
			return
		}

		target := patterns[request]
		diff := current ^ target
		fmt.Fprintln(out, bits.OnesCount64(diff))
		for diff != 0 {
			j := bits.TrailingZeros64(diff)
			visible := 2*j + int((current>>j)&1)
			fmt.Fprintln(out, visible, K-1)
			diff &= diff - 1
		}
		current = target
		out.Flush()
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
