package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strconv"
)

func main() {
	fs := NewFastScanner(os.Stdin)
	out := bufio.NewWriterSize(os.Stdout, 1<<20)
	defer out.Flush()

	N, M, K := fs.NextInt(), fs.NextInt(), fs.NextInt()

	A := make([]int64, N)
	B := make([]int, N)
	for i := 0; i < N; i++ {
		A[i] = fs.NextInt64()
		B[i] = int(fs.NextInt64())
	}

	DEQUE := make([]Deque, M+1)
	DP := make([]int64, M+1)
	ANSWER := int64(0)

	for i := 0; i < N; i++ {
		limit := i - K
		if limit < 0 {
			limit = 0
		}
		for c := 0; c <= M; c++ {
			DEQUE[c].popExpired(limit)
			DP[c] = negInf
		}

		bi := B[i]
		ai := A[i]
		if bi <= M {
			for c := bi; c <= M; c++ {
				prev := DEQUE[c-bi].max()
				if prev < 0 {
					prev = 0
				}
				DP[c] = ai + prev
			}
		}

		for c := 0; c <= M; c++ {
			if DP[c] > ANSWER {
				ANSWER = DP[c]
			}
			if DP[c] >= 0 {
				DEQUE[c].push(i, DP[c])
			}
		}
	}

	fmt.Fprintln(out, ANSWER)
}

const negInf int64 = -1 << 60

type pair struct {
	idx int
	val int64
}

type Deque struct {
	items []pair
	head  int
}

func (d *Deque) popExpired(limit int) {
	for d.head < len(d.items) && d.items[d.head].idx < limit {
		d.head++
	}
	if d.head >= len(d.items) {
		d.items = d.items[:0]
		d.head = 0
		return
	}
	if d.head > 1024 && d.head*2 >= len(d.items) {
		d.items = append([]pair(nil), d.items[d.head:]...)
		d.head = 0
	}
}

func (d *Deque) max() int64 {
	if d.head < len(d.items) {
		return d.items[d.head].val
	}
	return negInf
}

func (d *Deque) push(idx int, val int64) {
	if d.head >= len(d.items) {
		d.items = d.items[:0]
		d.head = 0
	}
	for len(d.items) > d.head && d.items[len(d.items)-1].val <= val {
		d.items = d.items[:len(d.items)-1]
	}
	d.items = append(d.items, pair{idx: idx, val: val})
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
