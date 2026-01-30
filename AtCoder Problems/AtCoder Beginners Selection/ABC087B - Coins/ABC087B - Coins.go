package main

import(
	"fmt"
)

func main() {
	var A int
	fmt.Scan(&A)

	var B int
	fmt.Scan(&B)
	
	var C int
	fmt.Scan(&C)

	var X int
	fmt.Scan(&X)

	count := 0

	for i := 0; i <= A; i++ {
		for j := 0; j <= B; j++ {
			for k := 0; k <= C; k++ {
				if i * 500 + j * 100 + k * 50 == X {
					count++
				}
			}
		}
	}
	fmt.Println(count)
}