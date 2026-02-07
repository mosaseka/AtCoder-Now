package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"sort"
	"strconv"
)

func main() {
	fs := NewFastScanner(os.Stdin)
	out := bufio.NewWriterSize(os.Stdout, 1<<20)
	defer out.Flush()

	N := fs.NextInt()
	A := make([]int64, N)
	var SUM int64 = 0
	var A_MAX int64 = 0

	for i := 0; i < N; i++ {
		A[i] = fs.NextInt64()
		SUM += A[i]
		if A[i] > A_MAX {
			A_MAX = A[i]
		}
	}

	sort.Slice(A, func(i, j int) bool { return A[i] < A[j] })

	divisors := []int64{}
	for i := int64(1); i*i <= SUM; i++ {
		if SUM%i == 0 {
			if i >= A_MAX {
				divisors = append(divisors, i)
			}
			if i*i != SUM {
				L := SUM / i
				if L >= A_MAX {
					divisors = append(divisors, L)
				}
			}
		}
	}

	ANSWER := []int64{}

	used := make([]bool, N)

	for _, L := range divisors {
		if checkL(L, A, used) {
			ANSWER = append(ANSWER, L)
		}
	}

	sort.Slice(ANSWER, func(i, j int) bool { return ANSWER[i] < ANSWER[j] })

	for i, ans := range ANSWER {
		if i > 0 {
			fmt.Fprint(out, " ")
		}
		fmt.Fprint(out, ans)
	}
	fmt.Fprintln(out)
}

func checkL(L int64, A []int64, used []bool) bool {
	n := len(A)

	for i := range used {
		used[i] = false
	}

	for i := 0; i < n; i++ {
		if A[i] == L {
			used[i] = true
		}
	}

	lo := 0
	hi := n - 1
	for lo < hi {
		for lo < hi && used[lo] {
			lo++
		}
		for lo < hi && used[hi] {
			hi--
		}
		if lo >= hi {
			break
		}
		s := A[lo] + A[hi]
		if s == L {
			used[lo] = true
			used[hi] = true
			lo++
			hi--
		} else if s < L {
			lo++
		} else {
			hi--
		}
	}

	for i := 0; i < n; i++ {
		if !used[i] {
			return false
		}
	}
	return true
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
