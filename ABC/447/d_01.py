from bisect import bisect_right

S = str(input())

POS_A = [i for i, c in enumerate(S) if c == 'A']
POS_B = [i for i, c in enumerate(S) if c == 'B']
POS_C = [i for i, c in enumerate(S) if c == 'C']

def CHECK(MID):
  if MID == 0:
    return True
  if MID > len(POS_A) or MID > len(POS_B) or MID > len(POS_C):
    return False

  B_INDICES = []
  B_START = 0
  for i in range(MID):
    A = POS_A[i]
    BI = bisect_right(POS_B, A, B_START)
    if BI >= len(POS_B):
      return False
    B_INDICES.append(POS_B[BI])
    B_START = BI + 1

  C_START = 0
  for i in range(MID):
    B = B_INDICES[i]
    CI = bisect_right(POS_C, B, C_START)
    if CI >= len(POS_C):
      return False
    C_START = CI + 1

  return True

LO, HI = 0, min(len(POS_A), len(POS_B), len(POS_C))
while LO < HI:
  MID = (LO + HI + 1) // 2
  if CHECK(MID):
    LO = MID
  else:
    HI = MID - 1

print(LO)