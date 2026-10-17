package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strconv"
	// "github.com/emirpasic/gods/queues/priorityqueue"
	"math"
)

func boundedProduct(a, d int64, length int, limit int64) (int64, bool) {
	product := int64(1)
	term := a
	for i := 0; i < length; i++ {
		if product > limit/term {
			return 0, false
		}
		product *= term
		term += d
	}
	return product, true
}

func main() {
	fs := NewFastScanner(os.Stdin)
	out := bufio.NewWriterSize(os.Stdout, 1<<20)
	defer out.Flush()

	N := fs.NextInt64()
	var answer int64

	// 長さ3: 初項を固定し、二次不等式から公差の上限を求める。
	for a := int64(1); ; a++ {
		if _, ok := boundedProduct(a, 1, 3, N); !ok {
			break
		}
		m := N / a
		d := int64((math.Sqrt(float64(a*a+8*m)) - float64(3*a)) / 4)
		// 平方根の丸め誤差を、整数の積の判定で補正する。
		for d > 0 {
			if _, ok := boundedProduct(a, d, 3, N); ok {
				break
			}
			d--
		}
		for {
			if _, ok := boundedProduct(a, d+1, 3, N); !ok {
				break
			}
			d++
		}
		answer += d
	}

	// 長さ4: 積は公差について単調増加するので、上限を二分探索する。
	for a := int64(1); ; a++ {
		if _, ok := boundedProduct(a, 1, 4, N); !ok {
			break
		}
		low, high := int64(1), int64(2)
		for {
			if _, ok := boundedProduct(a, high, 4, N); !ok {
				break
			}
			high *= 2
		}
		for high-low > 1 {
			mid := low + (high-low)/2
			if _, ok := boundedProduct(a, mid, 4, N); ok {
				low = mid
			} else {
				high = mid
			}
		}
		answer += low
	}

	// 長さ5以上: 初項と公差を列挙し、積がNを超えるまで伸ばす。
	for a := int64(1); ; a++ {
		if _, ok := boundedProduct(a, 1, 5, N); !ok {
			break
		}
		for d := int64(1); ; d++ {
			product, ok := boundedProduct(a, d, 5, N)
			if !ok {
				break
			}
			answer++
			for next := a + 5*d; product <= N/next; next += d {
				product *= next
				answer++
			}
		}
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
