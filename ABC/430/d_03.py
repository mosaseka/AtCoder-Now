import bisect

N = int(input())
X = list(map(int, input().split()))
RES = 0
ST = []
MP = {}

bisect.insort(ST, 0)
bisect.insort(ST, X[0])
MP[0] = X[0]
MP[X[0]] = X[0]
RES += 2 * X[0]
print(RES)

for i in range(1, N):
  V = X[i]
  HIT = []
  J = bisect.bisect_left(ST, V)
  if J < len(ST):
    HIT.append(ST[J])
  if J > 0:
    HIT.append(ST[J - 1])
  if not (J < len(ST) and ST[J] == V):
    ST.insert(J, V)
  MP[V] = 2000000000
  for NX in HIT:
    RES -= MP[NX]
    MP[NX] = min(MP[NX], abs(NX - V))
    RES += MP[NX]
    MP[V] = min(MP[V], abs(NX - V))
  RES += MP[V]
  print(RES)