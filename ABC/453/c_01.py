N = int(input())
L_LIST = list(map(int, input().split()))

DP = {1: 0}

for i in range(N):
  DIST = 2 * L_LIST[i]
  DP2 = {}
  for position, value in DP.items():
    N_POS = position + DIST
    PLUS = 1 if position * N_POS < 0 else 0
    BEST = value + PLUS
    if N_POS not in DP2 or DP2[N_POS] < BEST:
      DP2[N_POS] = BEST
  
    N_POS = position - DIST
    PLUS = 1 if position * N_POS < 0 else 0
    BEST = value + PLUS
    if N_POS not in DP2 or DP2[N_POS] < BEST:
      DP2[N_POS] = BEST
  
  DP = DP2

print(max(DP.values()))