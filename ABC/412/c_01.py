T = int(input())
ANS = []
for i in range(T):
  N = int(input())
  S_LIST = list(map(int, input().split()))
  FIRST = S_LIST[0]
  FINAL = S_LIST[-1]
  MID = sorted(S_LIST[1:-1])
  S = [FIRST] + MID + [FINAL]
  POS = 0
  CNT = 1
  CUR = S[0]
  while POS < N - 1:
    LEFT = POS + 1
    RIGHT = N - 1
    NXT = POS
    while LEFT <= RIGHT:
      MID_IDX = (LEFT + RIGHT) // 2
      if S[MID_IDX] <= 2 * CUR:
        NXT = MID_IDX
        LEFT = MID_IDX + 1
      else:
        RIGHT = MID_IDX - 1
    if NXT == POS:
      CNT = -1
      break
    CUR = S[NXT]
    POS = NXT
    CNT += 1
  if CNT >= 2 and POS == N - 1:
    ANS.append(str(CNT))
  else:
    ANS.append("-1")
    
print('\n'.join(ANS))