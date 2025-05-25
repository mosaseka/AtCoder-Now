N, H, W = map(int, input().split())
SY, SX = map(int, input().split())
S = str(input())
C = [list(map(int, input().split())) for _ in range(H)]

SX -= 1
SY -= 1

for i in range(H):
  for j in range(W):
    if C[i][j] == 0:
      NOW = [i, j]
      break

for i in range(N):
  if S[i] == "F":
    SY -= 1
  elif S[i] == "B":
    SY += 1
  elif S[i] == "L":
    SX -= 1
  elif S[i] == "R":
    SX += 1
  print(C[SY][SX])
