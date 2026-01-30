package main

import (
	"fmt"
	"sort"
)

func main() {
	var N int
	fmt.Scan(&N)

	aList := make([]int, N)
	for i := 0; i < N; i++ {
		fmt.Scan(&aList[i])
	}

	sort.Sort(sort.Reverse(sort.IntSlice(aList)))

	var alice, bob int

	for i := 0; i < N; i++ {
		if i%2 == 0 {
			alice += aList[i]
		} else {
			bob += aList[i]
		}
	}
	fmt.Println(alice - bob)
}