package main

import(
	"fmt"
)

func main() {
	var N, Y int
	fmt.Scan(&N, &Y)

	for i := 0; i < N + 1; i++{
		for j := 0; j < N - i + 1; j++{
			k := (Y - 10000*i - 5000*j) / 1000
			if k >= 0 && i + j + k == N {
				fmt.Println(i, j, k)
				return
			}
		}
	}
	fmt.Println(-1, -1, -1)
}