package main

import (
  "bufio"
  "fmt"
  "io"
  "os"
  "sort"
  "strconv"
)

type Query struct {
  L, R, X int
}

func main() {
  fs := NewFastScanner(os.Stdin)
  out := bufio.NewWriterSize(os.Stdout, 1<<20)
  defer out.Flush()

  N, Q := fs.NextInt(), fs.NextInt()
  queries := make([]Query, Q)
  for i := range queries {
    queries[i] = Query{L: fs.NextInt(), R: fs.NextInt(), X: fs.NextInt()}
  }

  sort.Slice(queries, func(i, j int) bool {
    if queries[i].X != queries[j].X {
      return queries[i].X < queries[j].X
    }
    return queries[i].L < queries[j].L
  })

  diff := make([]int, N+2)
  for i := 0; i < Q; {
    x := queries[i].X
    l, r := queries[i].L, queries[i].R
    i++

    for i < Q && queries[i].X == x {
      q := queries[i]
      if q.L <= r {
        if q.R > r {
          r = q.R
        }
      } else {
        diff[l]++
        diff[r+1]--
        l, r = q.L, q.R
      }
      i++
    }

    diff[l]++
    diff[r+1]--
  }

  count := 0
  for i := 1; i <= N; i++ {
    count += diff[i]
    fmt.Fprintln(out, count)
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
