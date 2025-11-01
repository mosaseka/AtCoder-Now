import bisect

def nearest(X, ST):
  I = bisect.bisect_left(ST, X)
  RESV = 2000000000
  if I > 0:
    RESV = min(RESV, X - ST[I - 1])
  if I + 1 < len(ST):
    RESV = min(RESV, ST[I + 1] - X)
  return RESV

N = int(input())
X = list(map(int, input().split()))
RES = 0
ST = []

bisect.insort(ST, 0)
bisect.insort(ST, X[0])
RES += 2 * X[0]
print(RES)

for i in range(1, N):
  CUR = X[i]
  HIT = []
  J = bisect.bisect_left(ST, CUR)
  if J < len(ST):
    HIT.append(ST[J])
  if J > 0:
    HIT.append(ST[J - 1])
  for NX in HIT:
    RES -= nearest(NX, ST)
  J = bisect.bisect_left(ST, CUR)
  if J == len(ST) or ST[J] != CUR:
    ST.insert(J, CUR)
  HIT.append(CUR)
  for NX in HIT:
    RES += nearest(NX, ST)
  print(RES)