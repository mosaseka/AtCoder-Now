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

STACK = [(H, W, 0, 0)]
while STACK:
  TH, TW, OFF_R, OFF_C = STACK.pop()

  if PIECES.get((TH, TW)):
    PI = PIECES[(TH, TW)].pop()
    if not PIECES[(TH, TW)]:
      WIDTH_TO_HEIGHTS[TW].discard(TH)
      HEIGHT_TO_WIDTHS[TH].discard(TW)
    ANS_R[PI] = OFF_R
    ANS_C[PI] = OFF_C
    continue

  FOUND = False

  if TW in WIDTH_TO_HEIGHTS:
    for PH in list(WIDTH_TO_HEIGHTS[TW]):
      if PH < TH and PIECES.get((PH, TW)):
        PI = PIECES[(PH, TW)].pop()
        if not PIECES[(PH, TW)]:
          WIDTH_TO_HEIGHTS[TW].discard(PH)
          HEIGHT_TO_WIDTHS[PH].discard(TW)
        ANS_R[PI] = OFF_R
        ANS_C[PI] = OFF_C
        STACK.append((TH - PH, TW, OFF_R + PH, OFF_C))
        FOUND = True
        break

  if not FOUND and TH in HEIGHT_TO_WIDTHS:
    for PW in list(HEIGHT_TO_WIDTHS[TH]):
      if PW < TW and PIECES.get((TH, PW)):
        PI = PIECES[(TH, PW)].pop()
        if not PIECES[(TH, PW)]:
          WIDTH_TO_HEIGHTS[PW].discard(TH)
          HEIGHT_TO_WIDTHS[TH].discard(PW)
        ANS_R[PI] = OFF_R
        ANS_C[PI] = OFF_C
        STACK.append((TH, TW - PW, OFF_R, OFF_C + PW))
        break

OUT = []
for i in range(N):
  OUT.append(f"{ANS_R[i] + 1} {ANS_C[i] + 1}")
print('\n'.join(OUT))