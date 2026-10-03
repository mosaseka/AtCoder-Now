package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strconv"
	// "github.com/emirpasic/gods/queues/priorityqueue"
)

type input struct {
	t, u, v int
}

func main() {
	fs := NewFastScanner(os.Stdin)
	out := bufio.NewWriterSize(os.Stdout, 1<<20)
	defer out.Flush()

	N, Q := fs.NextInt(), fs.NextInt()

	graph := make([][]int, N)
	reverseGraph := make([][]int, N)
	strictEdges := make([]input, 0, Q)
	for i := 0; i < Q; i++ {
		t, u, v := fs.NextInt(), fs.NextInt()-1, fs.NextInt()-1
		graph[u] = append(graph[u], v)
		reverseGraph[v] = append(reverseGraph[v], u)
		if t != 0 {
			strictEdges = append(strictEdges, input{t, u, v})
		}
	}

	ans := SCCValues(graph, reverseGraph)
	for _, edge := range strictEdges {
		if ans[edge.u] == ans[edge.v] {
			fmt.Fprintln(out, "No")
			return
		}
	}

	fmt.Fprintln(out, "Yes")
	for i, value := range ans {
		if i > 0 {
			fmt.Fprint(out, " ")
		}
		fmt.Fprint(out, value)
	}
	fmt.Fprintln(out)
}

// SCCValues は Kosaraju 法で強連結成分をトポロジカル順に番号付けする。
// 再帰を使わず、各頂点に所属成分の番号（1 始まり）を返す。
func SCCValues(graph, reverseGraph [][]int) []int {
	n := len(graph)
	visited := make([]bool, n)
	nextEdge := make([]int, n)
	order := make([]int, 0, n)
	stack := make([]int, 0, n)

	// 元のグラフで DFS の帰りがけ順を求める。
	for start := 0; start < n; start++ {
		if visited[start] {
			continue
		}
		visited[start] = true
		stack = append(stack, start)
		for len(stack) > 0 {
			v := stack[len(stack)-1]
			if nextEdge[v] < len(graph[v]) {
				to := graph[v][nextEdge[v]]
				nextEdge[v]++
				if !visited[to] {
					visited[to] = true
					stack = append(stack, to)
				}
			} else {
				order = append(order, v)
				stack = stack[:len(stack)-1]
			}
		}
	}

	// 帰りがけ順の逆順に、逆グラフで到達できる頂点をまとめる。
	ans := make([]int, n)
	componentID := 0
	for i := len(order) - 1; i >= 0; i-- {
		start := order[i]
		if ans[start] != 0 {
			continue
		}
		componentID++
		ans[start] = componentID
		stack = append(stack, start)
		for len(stack) > 0 {
			v := stack[len(stack)-1]
			stack = stack[:len(stack)-1]
			for _, to := range reverseGraph[v] {
				if ans[to] == 0 {
					ans[to] = componentID
					stack = append(stack, to)
				}
			}
		}
	}
	return ans
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
