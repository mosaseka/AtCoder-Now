from collections import deque

H, W = map(int, input().split())
S = [list(input()) for _ in range(H)]
DIRECTIONS = [(1, 0, "^"), (-1, 0, "v"), (0, 1, "<"), (0, -1, ">")]
QUEUE = deque()
DIST = [[-1] * W for _ in range(H)]
ARROWS = [[""] * W for _ in range(H)]

for i in range(H):
  for j in range(W):
    if S[i][j] == "E":
      QUEUE.append((i, j))
      DIST[i][j] = 0

while QUEUE:
  x, y = QUEUE.popleft()
  for dx, dy, arrow in DIRECTIONS:
    DX, DY = x + dx, y + dy
    if 0 <= DX < H and 0 <= DY < W and S[DX][DY] == "." and DIST[DX][DY] == -1:
      DIST[DX][DY] = DIST[x][y] + 1
      ARROWS[DX][DY] = arrow
      QUEUE.append((DX, DY))

for i in range(H):
  for j in range(W):
    if S[i][j] == ".":
      S[i][j] = ARROWS[i][j]

for i in S:
  print("".join(i))