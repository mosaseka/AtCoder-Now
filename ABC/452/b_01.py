H, W = map(int, input().split())

GRID = [["."] * W for _ in range(H)]

for i in range(H):
  for j in range(W):
    if i == 0:
      GRID[i][j] = "#"
    elif i == H - 1:
      GRID[i][j] = "#"
    elif j == 0:
      GRID[i][j] = "#"
    elif j == W - 1:
      GRID[i][j] = "#"

for i in range(H):
  print("".join(GRID[i]))