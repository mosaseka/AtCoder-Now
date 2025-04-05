from math import isqrt

N = int(input())
ANSWER = 0

for a in range(1, 61):
    ANSWER += (isqrt(N // (2**a)) + 1) // 2

print(ANSWER)