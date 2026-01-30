package main

import (
	"fmt"
	"strconv"
)

func main() {
	var N, A, B int
	fmt.Scan(&N, &A, &B)

	ans := 0

	for i := 1; i <= N; i++ {
		sum := 0
		check := strconv.Itoa(i)
		for j := 0; j < len(check); j++ {
			digit := int(check[j] - '0')
			sum += digit
		}
		if A <= sum && sum <= B {
			ans += i
		}
	}
	fmt.Println(ans)
}