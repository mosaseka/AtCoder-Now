from collections import deque

H, W = map(int, input().split())
GRID = [input().strip() for _ in range(H)]

SEEN = [[False] * W for _ in range(H)]
ANSWER = 0

for i in range(H):
  for j in range(W):
    if GRID[i][j] == "#" or SEEN[i][j]:
      continue

    QUEUE = deque([(i, j)])
    SEEN[i][j] = True
    TOUCHES_BORDER = i == 0 or i == H - 1 or j == 0 or j == W - 1

    while QUEUE:
      ROW, COL = QUEUE.popleft()

      for D_ROW, D_COL in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        NEXT_ROW = ROW + D_ROW
        NEXT_COL = COL + D_COL

        if not (0 <= NEXT_ROW < H and 0 <= NEXT_COL < W):
          continue
        if GRID[NEXT_ROW][NEXT_COL] == "#" or SEEN[NEXT_ROW][NEXT_COL]:
          continue

        SEEN[NEXT_ROW][NEXT_COL] = True
        if NEXT_ROW == 0 or NEXT_ROW == H - 1 or NEXT_COL == 0 or NEXT_COL == W - 1:
          TOUCHES_BORDER = True
        QUEUE.append((NEXT_ROW, NEXT_COL))

    if not TOUCHES_BORDER:
      ANSWER += 1

print(ANSWER)