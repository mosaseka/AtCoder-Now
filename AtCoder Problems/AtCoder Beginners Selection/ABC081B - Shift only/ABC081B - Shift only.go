package main

import(
	"fmt"
)

func main() {
	var n int
	fmt.Scan(&n)

	var a_list []int
	for i := 0; i < n; i++ {
		var a int
		fmt.Scan(&a)
		a_list = append(a_list, a)
	}

	flag := false
	ans := 0

	for {
		for i := 0; i < n; i++{
			if a_list[i] % 2 != 0 {
				flag = true
				break
			}
		}
		if flag {
			break
		}
		for i := 0; i < n; i++{
			a_list[i] /= 2
		}
		ans++
	}
	fmt.Println(ans)
}