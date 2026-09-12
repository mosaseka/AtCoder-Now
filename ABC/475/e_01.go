package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strconv"
)

type Node struct {
	next [2]int32
	cnt  int32
}

var (
	N, M, K int
	W       int
	bits    []uint64
	trie    []Node
)

func main() {
	fs := NewFastScanner(os.Stdin)
	out := bufio.NewWriterSize(os.Stdout, 1<<20)
	defer out.Flush()

	N, M, K = fs.NextInt(), fs.NextInt(), fs.NextInt()
	T := fs.Next()

	W = (K + 63) / 64
	bits = make([]uint64, N*W)
	trie = make([]Node, 1, N*K+1)

	for i := 0; i < N; i++ {
		S := fs.Next()
		for j := 0; j < K; j++ {
			if S[j] == T[j] {
				setBit(i, j)
			}
		}
		addPath(i, 1)
	}

	Q := fs.NextInt()

	for q := 0; q < Q; q++ {
		i, j := fs.NextInt()-1, fs.NextInt()-1
		addPath(i, -1)
		flipBit(i, j)
		addPath(i, 1)
		if canPass(i) {
			fmt.Fprintln(out, "Yes")
		} else {
			fmt.Fprintln(out, "No")
		}
	}
}

func bit(i, j int) int {
	if (bits[i*W+j/64]>>(uint(j)&63))&1 == 1 {
		return 1
	}
	return 0
}

func setBit(i, j int) {
	bits[i*W+j/64] |= 1 << (uint(j) & 63)
}

func flipBit(i, j int) {
	bits[i*W+j/64] ^= 1 << (uint(j) & 63)
}

func addPath(i int, delta int32) {
	v := int32(0)
	trie[v].cnt += delta
	for j := 0; j < K; j++ {
		b := bit(i, j)
		if trie[v].next[b] == 0 {
			trie = append(trie, Node{})
			trie[v].next[b] = int32(len(trie) - 1)
		}
		v = trie[v].next[b]
		trie[v].cnt += delta
	}
}

func countChild(v int32, b int) int {
	to := trie[v].next[b]
	if to == 0 {
		return 0
	}
	return int(trie[to].cnt)
}

func canPass(i int) bool {
	v := int32(0)
	passed := 0
	for j := 0; j < K; j++ {
		correct := countChild(v, 1)
		me := bit(i, j)
		if passed+correct <= M {
			if me == 1 {
				return true
			}
			passed += correct
			v = trie[v].next[0]
		} else {
			if me == 0 {
				return false
			}
			v = trie[v].next[1]
		}
	}
	return false
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
