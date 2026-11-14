package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strconv"
	// "github.com/emirpasic/gods/queues/priorityqueue"
)

type MinMax struct {
	minimum int
	maximum int
}

func toMinMax(x int) MinMax {
	if x == -1 {
		return MinMax{minimum: 1_000_001, maximum: 0}
	}
	return MinMax{minimum: x, maximum: x}
}

type SegmentTree struct {
	data []interface{}
	n    int
	e    interface{}
	op   func(interface{}, interface{}) interface{}
}

func NewSegmentTree(n int, e interface{}, op func(interface{}, interface{}) interface{}) *SegmentTree {
	segtree := new(SegmentTree)
	segtree.e = e
	segtree.op = op
	segtree.n = 1
	for segtree.n < n {
		segtree.n *= 2
	}
	segtree.data = make([]interface{}, segtree.n*2-1)
	for i := range segtree.data {
		segtree.data[i] = segtree.e
	}
	return segtree
}

func (segtree *SegmentTree) Build(values []interface{}) {
	for i, value := range values {
		segtree.data[segtree.n-1+i] = value
	}
	for i := segtree.n - 2; i >= 0; i-- {
		segtree.data[i] = segtree.op(segtree.data[i*2+1], segtree.data[i*2+2])
	}
}

func (segtree *SegmentTree) Update(idx int, x interface{}) {
	idx += segtree.n - 1
	segtree.data[idx] = x
	for 0 < idx {
		idx = (idx - 1) / 2
		segtree.data[idx] = segtree.op(segtree.data[idx*2+1], segtree.data[idx*2+2])
	}
}

func (segtree *SegmentTree) query(begin, end, idx, a, b int) interface{} {
	if b <= begin || end <= a {
		return segtree.e
	}
	if begin <= a && b <= end {
		return segtree.data[idx]
	}
	v1 := segtree.query(begin, end, idx*2+1, a, (a+b)/2)
	v2 := segtree.query(begin, end, idx*2+2, (a+b)/2, b)
	return segtree.op(v1, v2)
}

func (segtree *SegmentTree) Query(begin, end int) interface{} {
	return segtree.query(begin, end, 0, 0, segtree.n)
}

func main() {
	fs := NewFastScanner(os.Stdin)
	out := bufio.NewWriterSize(os.Stdout, 1<<20)
	defer out.Flush()

	N, Q := fs.NextInt(), fs.NextInt()

	e := MinMax{minimum: 1_000_001, maximum: 0}
	segtree := NewSegmentTree(N, e, func(a, b interface{}) interface{} {
		left, right := a.(MinMax), b.(MinMax)
		return MinMax{
			minimum: min(left.minimum, right.minimum),
			maximum: max(left.maximum, right.maximum),
		}
	})
	values := make([]interface{}, N)
	for i := 0; i < N; i++ {
		values[i] = toMinMax(fs.NextInt())
	}
	segtree.Build(values)

	for q := 0; q < Q; q++ {
		index := fs.NextInt()
		switch index {
		case 1:
			i, x := fs.NextInt(), fs.NextInt()
			segtree.Update(i-1, toMinMax(x))
		case 2:
			l, r := fs.NextInt(), fs.NextInt()
			result := segtree.Query(l-1, r).(MinMax)
			if result.maximum == 0 || result.minimum == result.maximum {
				fmt.Fprintln(out, "Yes")
			} else {
				fmt.Fprintln(out, "No")
			}
		}
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
