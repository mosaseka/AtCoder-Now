from math import gcd
from functools import cmp_to_key

N, Q = map(int, input().split())
XY = [list(map(int, input().split())) for _ in range(N)]

A = [-1] * N
B = []
C = []

for i in range(N):
  X, Y = XY[i]
  M = gcd(abs(X), abs(Y))
  A[i] = (X//M, Y//M)
  if X == 0:
    if Y > 0:
      B.append((X//M, Y//M))
    else:
      C.append((X//M, Y//M))
  elif X > 0:
    B.append((X//M, Y//M))
  else:
    C.append((X//M, Y//M))

def F(R1, R2):
  X1, Y1 = R1
  X2, Y2 = R2
  return -(X2 * Y1 - Y2 * X1)

B.sort(key=cmp_to_key(F))
C.sort(key=cmp_to_key(F))

ANS = B + C
D = {}
E = {}

for i in range(N):
  X, Y = ANS[i]
  if (X, Y) not in D:
    D[(X, Y)] = i
  E[(X, Y)] = i + 1

for _ in range(Q):
  A_IDX, B_IDX = map(lambda x: int(x) - 1, input().split())
  IDX0 = D[A[A_IDX]]
  IDX1 = E[A[B_IDX]]
  RESULT = (IDX1 - IDX0) % N
  if RESULT == 0:
    RESULT = N
  print(RESULT)