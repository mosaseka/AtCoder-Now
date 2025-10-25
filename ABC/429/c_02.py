from collections import Counter

N = int(input())
A = list(map(int, input().split()))
ANSWER = 0

COUNT = Counter(A)

for v, c in COUNT.items():
  if c >= 2:
    ANSWER += c * (c - 1) // 2 * (N - c)

print(ANSWER)