package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strconv"
)

var e [1000000][]int
var used [1000000]int
var cnt int

func dfs(s int, v int) {
	if used[v] == s {
		return
	}
	used[v] = s
	cnt++
	for _, next := range e[v] {
		dfs(s, next)
	}
}

func main() {
	fs := NewFastScanner(os.Stdin)
	out := bufio.NewWriterSize(os.Stdout, 1<<20)
	defer out.Flush()

	dx := [4]int{0, 0, 1, -1}
	dy := [4]int{1, -1, 0, 0}

	h := fs.NextInt()
	w := fs.NextInt()
	ans := 0

	s := make([]string, h)
	for i := 0; i < h; i++ {
		s[i] = fs.Next()
	}

	for i := 0; i < h; i++ {
		for j := 0; j < w; j++ {
			if s[i][j] == '#' {
				continue
			}
			can := true
			for k := 0; k < 4; k++ {
				ni := i + dx[k]
				nj := j + dy[k]
				if ni >= 0 && ni < h && nj >= 0 && nj < w {
					e[i*w+j] = append(e[i*w+j], ni*w+nj)
					if s[ni][nj] == '#' {
						can = false
					}
				}
			}
			if !can {
				e[i*w+j] = nil
			}
		}
	}

	for i := 0; i < h*w; i++ {
		used[i] = -1
	}

	for i := 0; i < h; i++ {
		for j := 0; j < w; j++ {
			idx := i*w + j
			if s[i][j] == '.' && used[idx] < 0 {
				cnt = 0
				dfs(idx, idx)
				if cnt > ans {
					ans = cnt
				}
			}
		}
	}

	fmt.Fprintln(out, ans)
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