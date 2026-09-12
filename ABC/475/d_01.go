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

	s := fs.Next()

	var l, r uint32
	if len(s) == 1 {
		l, r = 2, 9
	} else {
		l = 1
		for i := 0; i < len(s)-1; i++ {
			l *= 10
		}
		r = l*10 - 1
	}

	answer := -1
	primes := EnumeratePrimesInRange(l, r)
	for _, p := range primes {
		t := strconv.Itoa(int(p))

		charToDigit := make([]int, 26)
		digitToChar := make([]int, 10)
		for i := 0; i < 26; i++ {
			charToDigit[i] = -1
		}
		for i := 0; i < 10; i++ {
			digitToChar[i] = -1
		}

		ok := true
		for i := 0; i < len(s); i++ {
			c := int(s[i] - 'a')
			d := int(t[i] - '0')

			if charToDigit[c] != -1 && charToDigit[c] != d {
				ok = false
				break
			}
			if digitToChar[d] != -1 && digitToChar[d] != c {
				ok = false
				break
			}

			charToDigit[c] = d
			digitToChar[d] = c
		}

		if ok {
			answer = int(p)
			break
		}
	}

	fmt.Fprintln(out, answer)
}

type PrimeGenerator struct {
	Next func() uint32
}

func NewPrimeGenerator() *PrimeGenerator {
	primeGenerator := PrimeGenerator{}

	multiples := map[uint32]uint32{}
	var num uint32
	var d uint32

	primeGenerator.Next = func() uint32 {
		if num == 0 {
			num = 1
			return 2
		}
		if d == 0 {
			d = 4
			return 3
		}

		for {
			num += d
			d = 6 - d
			var k uint32 = 2

			factor, hasFactor := multiples[num]
			if hasFactor {
				delete(multiples, num)
				if (num+factor)%3 == 0 {
					k = 1
				}
			} else {
				factor = num
			}

			for newNum := num + (factor << k); ; newNum += factor << k {
				if _, hasNewFactor := multiples[newNum]; !hasNewFactor {
					multiples[newNum] = factor
					break
				}
				k ^= 3
			}

			if !hasFactor {
				return num
			}
		}
	}

	return &primeGenerator
}

func EnumeratePrimes(n uint32) []uint32 {
	return EnumeratePrimesInRange(2, n)
}

func EnumeratePrimesInRange(l, r uint32) []uint32 {
	primes := make([]uint32, 0)
	if l > r || r < 2 {
		return primes
	}
	if l < 2 {
		l = 2
	}

	primeGenerator := NewPrimeGenerator()
	for {
		p := primeGenerator.Next()
		if p > r {
			break
		}
		if p >= l {
			primes = append(primes, p)
		}
	}
	return primes
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
