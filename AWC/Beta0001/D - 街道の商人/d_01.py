from collections import deque

NEG_INF = -1 << 60

N, M, K = map(int, input().split())

A = []
B = []
for i in range(N):
  a, b = map(int, input().split())
  A.append(a)
  B.append(b)

DEQUE = [deque() for _ in range(M + 1)]
DP = [NEG_INF] * (M + 1)
ANSWER = 0

for i in range(N):
  LIMIT = max(0, i - K)
  
  for c in range(M + 1):
    while DEQUE[c] and DEQUE[c][0][0] < LIMIT:
      DEQUE[c].popleft()
    DP[c] = NEG_INF
  
  BI = B[i]
  AI = A[i]
  
  if BI <= M:
    for c in range(BI, M + 1):
      PREV = DEQUE[c - BI][0][1] if DEQUE[c - BI] else NEG_INF
      if PREV < 0:
        PREV = 0
      DP[c] = AI + PREV
  
  for c in range(M + 1):
    if DP[c] > ANSWER:
      ANSWER = DP[c]
    if DP[c] >= 0:
      while DEQUE[c] and DEQUE[c][-1][1] <= DP[c]:
        DEQUE[c].pop()
      DEQUE[c].append((i, DP[c]))

print(ANSWER)