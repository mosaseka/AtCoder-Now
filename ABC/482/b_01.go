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

func main() {
	fs := NewFastScanner(os.Stdin)
	out := bufio.NewWriterSize(os.Stdout, 1<<20)
	defer out.Flush()

	BINGO := make([][]bool, 5)

	for i := 0; i < 5; i++ {
		S := fs.Next()
		for j := 0; j < 5; j++ {
			if S[j] == 'o' {
				BINGO[i] = append(BINGO[i], true)
			} else {
				BINGO[i] = append(BINGO[i], false)
			}
		}
	}

	answer := math.MaxInt32

	for row := 0; row < 5; row++ {
		count := 0
		for col := 0; col < 5; col++ {
			if !BINGO[row][col] {
				count++
			}
		}
		if count < answer {
			answer = count
		}
	}

	for col := 0; col < 5; col++ {
		count := 0
		for row := 0; row < 5; row++ {
			if !BINGO[row][col] {
				count++
			}
		}
		if count < answer {
			answer = count
		}
	}

	count := 0
	for i := 0; i < 5; i++ {
		if !BINGO[i][i] {
			count++
		}
	}
	if count < answer {
		answer = count
	}

	count = 0
	for i := 0; i < 5; i++ {
		if !BINGO[i][4-i] {
			count++
		}
	}
	if count < answer {
		answer = count
	}

	fmt.Fprint(out, answer)
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
