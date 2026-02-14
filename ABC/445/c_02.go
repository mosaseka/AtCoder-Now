package main

import (
	"bufio"
	"fmt"
	"io"
	"math/big"
	"os"
	"strconv"
)

func main() {
	fs := NewFastScanner(os.Stdin)
	out := bufio.NewWriterSize(os.Stdout, 1<<20)
	defer out.Flush()

	N := fs.NextInt64()
	A_LIST := make([]int64, N)
	for i := 0; i < int(N); i++ {
		A_LIST[i] = fs.NextInt64()
	}

	FINAL := make([]int64, N+1)

	TARGET := new(big.Int)
	TARGET.Exp(big.NewInt(10), big.NewInt(100), nil)

	for i := int64(1); i <= N; i++ {
		PATH := make([]int64, 0)
		VISITED := make(map[int64]int)
		NOW := i

		for {
			if _, CHECK := VISITED[NOW]; CHECK {
				break
			}
			VISITED[NOW] = len(PATH)
			PATH = append(PATH, NOW)
			NOW = A_LIST[NOW-1]
		}

		CYCLE_START := VISITED[NOW]
		CYCLE_LEN := len(PATH) - CYCLE_START

		cycleStart := big.NewInt(int64(CYCLE_START))
		cycleLen := big.NewInt(int64(CYCLE_LEN))

		DIFF := new(big.Int).Sub(TARGET, cycleStart)
		REMAIN := new(big.Int).Mod(DIFF, cycleLen)
		FINAL[i] = PATH[CYCLE_START+int(REMAIN.Int64())]
	}

	for i := int64(1); i <= N; i++ {
		fmt.Fprintln(out, FINAL[i])
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
