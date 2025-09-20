T = int(input())

for _ in range(T):
  H, W = map(int, input().split())
  S = [list(input().strip()) for _ in range(H)]

  if H > W:
    S = list(map(list, zip(*S)))
    H, W = W, H

  if H <= 1 or W <= 1:
    print(0)
    continue

  COL = []
  for j in range(W):
    M = 0
    for i in range(H):
      if S[i][j] == '#':
        M |= 1 << i
    COL.append(M)

  MAXM = 1 << H

  PC = [0] * MAXM
  for m in range(1, MAXM):
    PC[m] = PC[m >> 1] + (m & 1)

  NOW_PAIR = [None] * W
  for j in range(W):
    ARR = [0] * MAXM
    CJ = COL[j]
    for nmask in range(MAXM):
      NOW = CJ & ~nmask
      ARR[nmask] = NOW & (NOW << 1)
    NOW_PAIR[j] = ARR

  INF = 10**9
  DP = [INF] * MAXM
  for nmask in range(MAXM):
    DP[nmask] = PC[nmask]

  for j in range(1, W):
    NDP = [INF] * MAXM

    PREV_PAIR = [0] * MAXM
    CJ_1 = COL[j - 1]
    for pmask in range(MAXM):
      PREV = CJ_1 & ~pmask
      PREV_PAIR[pmask] = PREV & (PREV << 1)

    NPJ = NOW_PAIR[j]
    for pmask in range(MAXM):
      CUR = DP[pmask]
      if CUR == INF:
        continue
      PP = PREV_PAIR[pmask]
      for nmask in range(MAXM):
        if (PP & NPJ[nmask]) == 0:
          VAL = CUR + PC[nmask]
          if VAL < NDP[nmask]:
            NDP[nmask] = VAL
    DP = NDP

  print(min(DP))