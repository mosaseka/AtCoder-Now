#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int abs_int(int a) {
	if (a < 0) {
		return -a;
	}
	return a;
}

int main(void) {
	int N;
	scanf("%d", &N);

	int tPast = 0, xPast = 0, yPast = 0;

	for (int i = 0; i < N; i++) {
		int t, x, y;
		scanf("%d %d %d", &t, &x, &y);

		int length = abs_int(x - xPast) + abs_int(y - yPast);
		int time = t - tPast;

		tPast = t;
		xPast = x;
		yPast = y;

		if (!(length <= time && length % 2 == time % 2)) {
			printf("No\n");
			return 0;
		}
	}

	printf("Yes\n");
	return 0;
}