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
	out := bufio.NewWriter(os.Stdout)
	defer out.Flush()

	T := fs.NextInt()

	for t := 0; t < T; t++ {
		N, C := fs.NextInt(), fs.NextInt()
		S_LIST := make([][]rune, N)
		for i := 0; i < N; i++ {
			S_LIST[i] = []rune(fs.Next())
		}

		C -= 1
		LOW := make([]int, N)
		for i := 0; i < N; i++ {
			LOW[i] = -1
		}

		for i := 0; i < N; i++ {
			for j := 0; j < N; j++ {
				if S_LIST[i][j] == '#' {
					LOW[j] = i
				}
			}
		}

		DP := make([][]int, N)
		for i := 0; i < N; i++ {
			DP[i] = make([]int, N)
		}

		for i := 0; i < N; i++ {
			DP[i][C] = 1
		}

		for i := N - 2; i >= 0; i-- {
			for j := 0; j < N; j++ {
				if DP[i][j] > 0 {
					continue
				}

				FLAG := false
				if DP[i+1][j] > 0 {
					FLAG = true
				}
				if j > 0 && DP[i+1][j-1] > 0 {
					FLAG = true
				}
				if j+1 < N && DP[i+1][j+1] > 0 {
					FLAG = true
				}

				if FLAG {
					if S_LIST[i][j] == '.' {
						DP[i][j] = 1
					} else {
						if LOW[j] == i {
							for k := 0; k <= i; k++ {
								DP[k][j] = 1
							}
						}
					}
				}
			}
		}

		for j := 0; j < N; j++ {
			fmt.Fprint(out, DP[0][j])
		}
		fmt.Fprintln(out)
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