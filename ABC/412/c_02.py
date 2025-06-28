T = int(input())
ANS = []
for _ in range(T):
  N = int(input())
  S_LIST = list(map(int, input().split()))
  FIRST = S_LIST[0]
  FINAL = S_LIST[-1]
  MID = sorted(S_LIST[1:-1])
  S = [FIRST] + MID + [FINAL]
  # dp[i]: S[i]を最後に使う並べ方の最小個数
  DP = [float('inf')] * N
  DP[0] = 1
  for i in range(N):
    if DP[i] == float('inf'):
      continue
    LEFT = i + 1
    RIGHT = N - 1
    NXT = i
    while LEFT <= RIGHT:
      MID_IDX = (LEFT + RIGHT) // 2
      if S[MID_IDX] <= 2 * S[i]:
        NXT = MID_IDX
        LEFT = MID_IDX + 1
      else:
        RIGHT = MID_IDX - 1
    for j in range(i + 1, NXT + 1):
      if DP[j] > DP[i] + 1:
        DP[j] = DP[i] + 1
  if DP[N - 1] != float('inf') and DP[N - 1] >= 2:
    ANS.append(str(DP[N - 1]))
  else:
    ANS.append("-1")
    
print('\n'.join(ANS))