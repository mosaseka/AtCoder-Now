N, K = map(int, input().split())
ANSWER = 0
SUM = 0

while SUM < K:
  SUM += N + ANSWER
  ANSWER += 1

print(ANSWER - 1)