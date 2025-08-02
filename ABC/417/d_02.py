from itertools import accumulate
import bisect

N = int(input())
P = [list(map(int, input().split())) for _ in range(N)]

M = max(p + a for p, a, _ in P)

DP = [[0] * (M + 1) for _ in range(N + 1)]

DP[N] = list(range(M + 1))

for i in reversed(range(N)):
  P_VAL, A, B = P[i]
  for j in range(M + 1):
    if j <= P_VAL:
      if j + A <= M:
        DP[i][j] = DP[i + 1][j + A]
      else:
        DP[i][j] = j + A
    else:
      DP[i][j] = DP[i + 1][j - min(j, B)]

SUM_B = list(accumulate(p[2] for p in P))

def ACCESS(X):
  if X <= M:
    return DP[0][X]
  
  IDX = bisect.bisect_left(SUM_B, X - M)
  if IDX == len(SUM_B):
    return X - SUM_B[-1]
  else:
    i = IDX + 1
    j = X - min(X, SUM_B[IDX])
    return DP[i][j]

Q = int(input())
for _ in range(Q):
  X = int(input())
  print(ACCESS(X))