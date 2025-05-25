H, W = map(int,input().split())
S = [list(map(int,input().split())) for _ in range(H)]
DP = [[0]*W for _ in range(H)]
NEXT = 0

for i in range(W):
  DP[H-1][i] = S[H-1][i]

for i in range(H-2, -1, -1):
  for j in range(W):
    NEXT = DP[i+1][j]
    if j > 0:
      NEXT = max(NEXT, DP[i+1][j-1])
    if j < W-1:
      NEXT = max(NEXT, DP[i+1][j+1])
    DP[i][j] = S[i][j] + NEXT

print(max(DP[0]))
