H, W = map(int, input().split())
C_LIST = [list(map(str, input())) for _ in range(H)]

TOP = H
BOTTOM = -1
LEFT = W
RIGHT = -1

for i in range(H):
  for j in range(W):
    if C_LIST[i][j] == "#":
      TOP = min(TOP, i)
      BOTTOM = max(BOTTOM, i)
      LEFT = min(LEFT, j)
      RIGHT = max(RIGHT, j)

for i in range(TOP, BOTTOM + 1):
  print(''.join(C_LIST[i][LEFT:RIGHT + 1]))