package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strconv"
	// "github.com/emirpasic/gods/queues/priorityqueue"
)

func main() {
	fs := NewFastScanner(os.Stdin)
	out := bufio.NewWriterSize(os.Stdout, 1<<20)
	defer out.Flush()

	Q := fs.NextInt()
	S := fs.Next()
	T := fs.Next()

	// KMP: T の各位置までの接頭辞と接尾辞が一致する最大長。
	N, M := len(S), len(T)
	pi := make([]int, M)
	for i, j := 1, 0; i < M; i++ {
		for j > 0 && T[i] != T[j] {
			j = pi[j-1]
		}
		if T[i] == T[j] {
			j++
		}
		pi[i] = j
	}

	// prefix[k] は、開始位置が 0 以上 k 未満の出現数。
	prefix := make([]int, N+1)
	for i, j := 0, 0; i < N; i++ {
		for j > 0 && S[i] != T[j] {
			j = pi[j-1]
		}
		if S[i] == T[j] {
			j++
		}
		if j == M {
			prefix[i-M+2]++
			j = pi[j-1]
		}
	}
	for i := 1; i <= N; i++ {
		prefix[i] += prefix[i-1]
	}

	for i := 0; i < Q; i++ {
		L, R := fs.NextInt(), fs.NextInt()

		if R-L+1 >= M && prefix[R-M+1]-prefix[L-1] > 0 {
			fmt.Fprintln(out, "Yes")
		} else {
			fmt.Fprintln(out, "No")
		}
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
