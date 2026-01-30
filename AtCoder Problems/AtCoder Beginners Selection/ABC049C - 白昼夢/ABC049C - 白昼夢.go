package main

import (
	"fmt"
)

func reverse(s string) string {
	r := []rune(s)
	for i, j := 0, len(r)-1; i < j; i, j = i+1, j-1 {
		r[i], r[j] = r[j], r[i]
	}
	return string(r)
}

func main() {
	var S string
	fmt.Scan(&S)

	divide := []string{"dream", "dreamer", "erase", "eraser"}
	for i := range divide {
		divide[i] = reverse(divide[i])
	}
	S = reverse(S)

	can := true
	for i := 0; i < len(S); {
		can2 := false
		for j := 0; j < 4; j++ {
			d := divide[j]
			if i+len(d) <= len(S) && S[i:i+len(d)] == d {
				can2 = true
				i += len(d)
				break
			}
		}
		if !can2 {
			can = false
			break
		}
	}

	if can {
		fmt.Println("YES")
	} else {
		fmt.Println("NO")
	}
}