from math import ceil

N, M = map(int, input().split())
ANSWER = 0

for i in range(N):
  A, B = map(int, input().split())
  if A >= M:
    CHECK = 0
  else:
    CHECK = ceil((M - A) / B)
  ANSWER = max(ANSWER, CHECK)

print(ANSWER)