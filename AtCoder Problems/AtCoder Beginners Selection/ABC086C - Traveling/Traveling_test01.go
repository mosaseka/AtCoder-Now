package main

import (
	"bufio"
	"fmt"
	"os"
)

type FastScanner struct {
	r *bufio.Reader
}

func NewFastScanner() *FastScanner {
	return &FastScanner{r: bufio.NewReaderSize(os.Stdin, 1<<20)}
}

func (fs *FastScanner) NextInt() int {
	sign, val := 1, 0
	c, _ := fs.r.ReadByte()
	for c <= ' ' {
		c, _ = fs.r.ReadByte()
	}
	if c == '-' {
		sign = -1
		c, _ = fs.r.ReadByte()
	}
	for c > ' ' {
		val = val*10 + int(c-'0')
		c, _ = fs.r.ReadByte()
	}
	return val * sign
}

func abs(a int) int {
	if a < 0 {
		return -a
	}
	return a
}

func main() {
	fs := NewFastScanner()
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