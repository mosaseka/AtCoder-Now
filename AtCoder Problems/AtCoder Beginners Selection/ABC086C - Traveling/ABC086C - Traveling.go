package main

import(
	"fmt"
)

func abs(a int) int {
	if a < 0 {
		return -a
	}
	return a
}

func main() {
	var N int
	fmt.Scan(&N)

	var tPast, xPast, yPast int

	for i := 0; i < N; i++ {
		var t, x, y int
		fmt.Scan(&t, &x, &y)

		length := abs(x - xPast) + abs(y - yPast)
		time := t - tPast

		tPast, xPast, yPast = t, x, y

		if length <= time && length % 2 == time % 2{
			// 
		} else{
			fmt.Println("No")
			return
		}
	}
	fmt.Println("Yes")
}