package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
	// "github.com/emirpasic/gods/queues/priorityqueue"
)

func main() {
	fs := NewFastScanner(os.Stdin)
	out := bufio.NewWriterSize(os.Stdout, 1<<20)
	defer out.Flush()

	N, Q := fs.NextInt(), fs.NextInt()

	type Query struct {
		typ   int
		pos   int
		color string
	}
	qry := make([]Query, 0, Q+1)
	qry = append(qry, Query{typ: 2, color: "a"})
	tile := make([]int, N)

	for i := 0; i < Q; i++ {
		t := fs.NextInt()
		if t == 1 {
			x := fs.NextInt() - 1
			tile[x] ^= 1
			qry = append(qry, Query{typ: 1, pos: x})
		} else {
			qry = append(qry, Query{typ: 2, color: fs.Next()})
		}
	}

	// Python の set に相当する集合。
	s := make(map[int]struct{})
	for i := 0; i < N; i++ {
		if tile[i] == 0 {
			s[i] = struct{}{}
		}
	}
	ans := make([]string, N)
	for k := len(qry) - 1; k >= 0; k-- {
		query := qry[k]
		if query.typ == 1 {
			x := query.pos
			if ans[x] == "" {
				if tile[x] == 0 {
					delete(s, x)
				} else {
					s[x] = struct{}{}
				}
			}
			tile[x] ^= 1
		} else {
			for i := range s {
				ans[i] = query.color
				delete(s, i)
			}
		}
	}
	fmt.Fprintln(out, strings.Join(ans, ""))
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
