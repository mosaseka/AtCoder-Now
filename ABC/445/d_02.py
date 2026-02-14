from collections import defaultdict

H, W, N = map(int, input().split())
HW_LIST = [list(map(int, input().split())) for _ in range(N)]

PIECES = defaultdict(list)
for i in range(N):
  PIECES[(HW_LIST[i][0], HW_LIST[i][1])].append(i)

ANS_R = [0] * N
ANS_C = [0] * N

WIDTH_TO_HEIGHTS = defaultdict(set)
HEIGHT_TO_WIDTHS = defaultdict(set)
for i in range(N):
  WIDTH_TO_HEIGHTS[HW_LIST[i][1]].add(HW_LIST[i][0])
  HEIGHT_TO_WIDTHS[HW_LIST[i][0]].add(HW_LIST[i][1])

def POP_PIECE(PH, PW):
  PI = PIECES[(PH, PW)].pop()
  if not PIECES[(PH, PW)]:
    WIDTH_TO_HEIGHTS[PW].discard(PH)
    HEIGHT_TO_WIDTHS[PH].discard(PW)
  return PI

def SOLVE(TH, TW, OFF_R, OFF_C):
  if PIECES.get((TH, TW)):
    PI = POP_PIECE(TH, TW)
    ANS_R[PI] = OFF_R
    ANS_C[PI] = OFF_C
    return True

  if TW in WIDTH_TO_HEIGHTS:
    for PH in list(WIDTH_TO_HEIGHTS[TW]):
      if PH < TH and PIECES.get((PH, TW)):
        PI = POP_PIECE(PH, TW)
        ANS_R[PI] = OFF_R
        ANS_C[PI] = OFF_C
        if SOLVE(TH - PH, TW, OFF_R + PH, OFF_C):
          return True
        PIECES[(PH, TW)].append(PI)
        WIDTH_TO_HEIGHTS[TW].add(PH)
        HEIGHT_TO_WIDTHS[PH].add(TW)
        break

  if TH in HEIGHT_TO_WIDTHS:
    for PW in list(HEIGHT_TO_WIDTHS[TH]):
      if PW < TW and PIECES.get((TH, PW)):
        PI = POP_PIECE(TH, PW)
        ANS_R[PI] = OFF_R
        ANS_C[PI] = OFF_C
        if SOLVE(TH, TW - PW, OFF_R, OFF_C + PW):
          return True
        PIECES[(TH, PW)].append(PI)
        WIDTH_TO_HEIGHTS[PW].add(TH)
        HEIGHT_TO_WIDTHS[TH].add(PW)
        break

  return False

SOLVE(H, W, 0, 0)

OUT = []
for i in range(N):
  OUT.append(f"{ANS_R[i] + 1} {ANS_C[i] + 1}")
print('\n'.join(OUT))