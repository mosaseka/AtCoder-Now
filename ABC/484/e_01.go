package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"sort"
	"strconv"
	// "github.com/emirpasic/gods/queues/priorityqueue"
)

type BIT struct {
	size int
	bit  []int64
}

func NewBIT(n int) *BIT {
	return &BIT{size: n, bit: make([]int64, n+1)}
}

func (b *BIT) Add(i int, x int64) {
	i++
	for i <= b.size {
		b.bit[i] += x
		i += i & -i
	}
}

func (b *BIT) Sum(i int) int64 {
	i++
	var s int64
	for i > 0 {
		s += b.bit[i]
		i -= i & -i
	}
	return s
}

func (b *BIT) RangeSum(l, r int) int64 {
	return b.Sum(r-1) - b.Sum(l-1)
}

func main() {
	fs := NewFastScanner(os.Stdin)
	out := bufio.NewWriterSize(os.Stdout, 1<<20)
	defer out.Flush()

	N := fs.NextInt()
	L, R := fs.NextInt64(), fs.NextInt64()

	A_LIST := make([]int64, N+1)
	for i := 0; i < N; i++ {
		A_LIST[i+1] = A_LIST[i] + fs.NextInt64()
	}

	values := append([]int64(nil), A_LIST...)
	sort.Slice(values, func(i, j int) bool { return values[i] < values[j] })
	uniqueCount := 0
	for _, v := range values {
		if uniqueCount == 0 || values[uniqueCount-1] != v {
			values[uniqueCount] = v
			uniqueCount++
		}
	}
	values = values[:uniqueCount]

	bit := NewBIT(len(values))
	zeroIndex := sort.Search(len(values), func(i int) bool { return values[i] >= 0 })
	bit.Add(zeroIndex, 1)

	var answer int64
	for j := 1; j <= N; j++ {
		lower, upper := A_LIST[j]-R, A_LIST[j]-L
		left := sort.Search(len(values), func(i int) bool { return values[i] >= lower })
		right := sort.Search(len(values), func(i int) bool { return values[i] > upper })
		answer += bit.RangeSum(left, right)

		index := sort.Search(len(values), func(i int) bool { return values[i] >= A_LIST[j] })
		bit.Add(index, 1)
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
