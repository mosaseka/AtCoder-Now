from collections import defaultdict

N = int(input())
A = list(map(int, input().split()))

COUNT = defaultdict(int)

for i in range(N):
  KEY = i + 1 + A[i]
  COUNT[KEY] += 1

ANSWER = 0

for j in range(N):
  KEY = j + 1 - A[j]
  ANSWER += COUNT.get(KEY, 0)

print(ANSWER)