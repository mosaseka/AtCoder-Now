from sortedcontainers import SortedList

N, D = map(int, input().split())
A_LIST = list(map(int, input().split()))

SL = SortedList()
ANS = 0
L = 0
BAD_COUNT = 0

for r in range(N):
  A = A_LIST[r]
  IDX = SL.bisect_left(A)
  if 0 < IDX < len(SL):
    if abs(SL[IDX] - SL[IDX - 1]) < D:
      BAD_COUNT -= 1
  if IDX < len(SL):
    if abs(A - SL[IDX]) < D:
      BAD_COUNT += 1
  if IDX > 0:
    if abs(A - SL[IDX - 1]) < D:
      BAD_COUNT += 1
  SL.add(A)

  while BAD_COUNT > 0:
    B = A_LIST[L]
    L += 1
    IDX2 = SL.index(B)
    if IDX2 > 0:
      if abs(B - SL[IDX2 - 1]) < D:
        BAD_COUNT -= 1
    if IDX2 < len(SL) - 1:
      if abs(B - SL[IDX2 + 1]) < D:
        BAD_COUNT -= 1
    if IDX2 > 0 and IDX2 < len(SL) - 1:
      if abs(SL[IDX2 - 1] - SL[IDX2 + 1]) < D:
        BAD_COUNT += 1
    SL.remove(B)

  ANS += r - L + 1

print(ANS)