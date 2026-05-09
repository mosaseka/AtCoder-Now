from bisect import bisect_left, bisect_right
from collections import defaultdict

N, M = map(int, input().split())

INF = 10 ** 9

BY_L = [[] for _ in range(N + 1)]
BY_R = [[] for _ in range(N + 1)]
COUNT = defaultdict(int)
MIN_R_AT_L = [INF] * (N + 2)

for _ in range(M):
  L, R = map(int, input().split())
  BY_L[L].append(R)
  BY_R[R].append(L)
  COUNT[(L, R)] += 1
  MIN_R_AT_L[L] = min(MIN_R_AT_L[L], R)

for i in range(1, N + 1):
  BY_L[i].sort()
  BY_R[i].sort()

SUF_MIN_R = [INF] * (N + 3)

for i in range(N, 0, -1):
  SUF_MIN_R[i] = min(SUF_MIN_R[i + 1], MIN_R_AT_L[i])

Q = int(input())
ANS = []

for _ in range(Q):
  S, T = map(int, input().split())

  if COUNT[(S, T)] > 0:
    FLAG = False

    FLAG |= COUNT[(S, T)] >= 2
    FLAG |= SUF_MIN_R[S + 1] <= T
    FLAG |= SUF_MIN_R[S] <= T - 1

    ANS.append("Yes" if FLAG else "No")
    continue

  FLAG = False

  RIGHT_ENDS = BY_L[S]
  POS_R = bisect_right(RIGHT_ENDS, T) - 1

  LEFT_ENDS = BY_R[T]
  POS_L = bisect_left(LEFT_ENDS, S)

  if POS_R >= 0 and POS_L < len(LEFT_ENDS):
    R1 = RIGHT_ENDS[POS_R]
    L2 = LEFT_ENDS[POS_L]
    FLAG |= L2 <= R1 + 1

  ANS.append("Yes" if FLAG else "No")

print("\n".join(ANS))