def CROSS(A, B):
  return A[0] * B[1] - A[1] * B[0]

def CMP(A, B):
  AH = (A[1] < 0) or (A[1] == 0 and A[0] < 0)
  BH = (B[1] < 0) or (B[1] == 0 and B[0] < 0)
  if AH != BH:
    return AH < BH
  return CROSS(A, B) > 0

N, Q = map(int, input().split())
PT = [tuple(map(int, input().split())) for _ in range(N)]

ORD = list(range(N))
ORD.sort(key=lambda i: (CMP(PT[i], PT[0]), CROSS(PT[i], PT[0]) if not CMP(PT[i], PT[0]) else -CROSS(PT[i], PT[0])))
ORD.sort(key=lambda i: PT[i], reverse=True)

ORD = list(range(N))
ORD.sort(key=lambda i: PT[i])
ORD.reverse()

def CMP_SORT(I, J):
  return CMP(PT[I], PT[J])

from functools import cmp_to_key
ORD = list(range(N))
ORD.sort(key=cmp_to_key(lambda i, j: -1 if CMP(PT[i], PT[j]) else 1))
ORD.reverse()

REV = [0] * N
for i in range(N):
  REV[ORD[i]] = i

L = [0] * N
R = [0] * N
L[0] = 0
R[N - 1] = N

for i in range(1, N):
  if CMP(PT[ORD[i]], PT[ORD[i - 1]]):
    L[i] = i
  else:
    L[i] = L[i - 1]

for i in range(N - 2, -1, -1):
  if CMP(PT[ORD[i + 1]], PT[ORD[i]]):
    R[i] = i + 1
  else:
    R[i] = R[i + 1]

for _ in range(Q):
  A, B = map(int, input().split())
  A -= 1
  B -= 1
  A = L[REV[A]]
  B = R[REV[B]]
  if A < B:
    print(B - A)
  else:
    print(N - A + B)