package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strconv"
)

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

// Java版と同じ: ASCII printable (33..126)
func isPrintableChar(c int) bool {
	return 33 <= c && c <= 126
}

// Java版 hasNext() 相当
func (fs *FastScanner) HasNext() bool {
	for fs.hasNextByte() && !isPrintableChar(int(fs.buffer[fs.ptr])) {
		fs.ptr++
	}
	return fs.hasNextByte()
}

// Java版 next() 相当
func (fs *FastScanner) Next() string {
	if !fs.HasNext() {
		panic("NoSuchElementException")
	}
	// StringBuilder相当: byte slice に append
	b := make([]byte, 0, 16)
	c := fs.readByte()
	for isPrintableChar(c) {
		b = append(b, byte(c))
		c = fs.readByte()
	}
	return string(b)
}

// Java版 nextLong() 相当
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

// Java版 nextInt() 相当（範囲チェック付き）
func (fs *FastScanner) NextInt() int {
	x := fs.NextInt64()
	if x < -2147483648 || x > 2147483647 {
		panic("NumberFormatException")
	}
	return int(x)
}

// Java版 nextDouble() 相当（strconvでパース）
func (fs *FastScanner) NextFloat64() float64 {
	s := fs.Next()
	v, err := strconv.ParseFloat(s, 64)
	if err != nil {
		panic("NumberFormatException")
	}
	return v
}

func abs(a int) int {
	if a < 0 {
		return -a
	}
	return a
}

func main() {
	fs := NewFastScanner(os.Stdin)
	out := bufio.NewWriterSize(os.Stdout, 1<<20)
	defer out.Flush()

	N := fs.NextInt()
	tPast, xPast, yPast := 0, 0, 0

	for i := 0; i < N; i++ {
		t := fs.NextInt()
		x := fs.NextInt()
		y := fs.NextInt()

		length := abs(x - xPast) + abs(y - yPast)
		time := t - tPast

		if length <= time && length%2 == time%2 {
			// OK
		} else {
			fmt.Fprintln(out, "No")
			return
		}
		tPast, xPast, yPast = t, x, y
	}
	fmt.Fprintln(out, "Yes")
}