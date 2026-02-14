H, W, N = map(int, input().split())
HW_LIST = [list(map(int, input().split())) for _ in range(N)]
PIECE = [(HW_LIST[i][0], HW_LIST[i][1], i) for i in range(N)]

def SOLVE(TH, TW, PC):
  if len(PC) == 1:
    return {PC[0][2]: (0, 0)}
  for k in range(len(PC)):
    PH, PW, PI = PC[k]
    if PW == TW and PH < TH:
      REST = PC[:k] + PC[k+1:]
      RH = TH - PH
      RR = SOLVE(RH, TW, REST)
      if RR is not None:
        ANS = {PI: (0, 0)}
        for IDX, (Y, X) in RR.items():
          ANS[IDX] = (Y + PH, X)
        return ANS
    if PH == TH and PW < TW:
      REST = PC[:k] + PC[k+1:]
      RW = TW - PW
      RR = SOLVE(TH, RW, REST)
      if RR is not None:
        ANS = {PI: (0, 0)}
        for IDX, (Y, X) in RR.items():
          ANS[IDX] = (Y, X + PW)
        return ANS
  return None

POS = SOLVE(H, W, PIECE)
if POS:
  OUT = []
  for i in range(N):
    Y, X = POS[i]
    OUT.append(f"{Y + 1} {X + 1}")
  print('\n'.join(OUT))