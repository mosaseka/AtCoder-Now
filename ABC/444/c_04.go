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
	A_LIST := make([]int64, N)
	var SUM int64 = 0
	var A_MAX int64 = 0

	for i := 0; i < N; i++ {
		A_LIST[i] = fs.NextInt64()
		SUM += A_LIST[i]
		if A_LIST[i] > A_MAX {
			A_MAX = A_LIST[i]
		}
	}

	BASE_COUNT := make(map[int64]int64)
	for _, a := range A_LIST {
		BASE_COUNT[a]++
	}

	// 約数を求める
	divisors := []int64{}

	for i := int64(1); i*i <= SUM; i++ {
		if SUM%i == 0 {
			if i >= A_MAX {
				divisors = append(divisors, i)
			}
			if i != SUM/i {
				L := SUM / i
				if L >= A_MAX {
					divisors = append(divisors, L)
				}
			}
		}
	}

	ANSWER := []int64{}

	for _, L := range divisors {
		COUNT := make(map[int64]int64, len(BASE_COUNT))
		for k, v := range BASE_COUNT {
			COUNT[k] = v
		}

		ok := true
		for a := range BASE_COUNT {
			if COUNT[a] == 0 {
				continue
			}

			if a == L {
				COUNT[a] = 0
			} else {
				need := L - a
				if need == a {
					if COUNT[a]%2 != 0 {
						ok = false
						break
					}
					COUNT[a] = 0
				} else {
					if COUNT[need] < COUNT[a] {
						ok = false
						break
					}
					COUNT[need] -= COUNT[a]
					COUNT[a] = 0
				}
			}
		}

		if ok {
			ANSWER = append(ANSWER, L)
		}
	}

	sort.Slice(ANSWER, func(i, j int) bool {
		return ANSWER[i] < ANSWER[j]
	})

	for i, ans := range ANSWER {
		if i > 0 {
			fmt.Fprint(out, " ")
		}
		fmt.Fprint(out, ans)
	}
	fmt.Fprintln(out)
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
