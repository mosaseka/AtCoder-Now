package main

import (
	"fmt"
)

func main() {
	var N int
	fmt.Scan(&N)

	dList := make([]int, N)
	for i := 0; i < N; i++ {
		fmt.Scan(&dList[i])
	}

	unique := make(map[int]bool)
	for _, d := range dList {
		unique[d] = true
	}

	fmt.Println(len(unique))
}