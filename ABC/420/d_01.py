from collections import deque

H, W = map(int, input().split())
A_LIST = [list(input()) for _ in range(H)]

START = None
GOAL = None
for i in range(H):
  for j in range(W):
    if A_LIST[i][j] == 'S':
      START = (i, j)
    elif A_LIST[i][j] == 'G':
      GOAL = (i, j)

#BFSでやる
QUEUE = deque([(START[0], START[1], 0, 0)])
VISITED = set()
VISITED.add((START[0], START[1], 0))

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

while QUEUE:
  x, y, SWITCH_STATE, DIST = QUEUE.popleft()
  if (x, y) == GOAL:
    print(DIST)
    exit()
  for dx, dy in DIRECTIONS:
    NX, NY = x + dx, y + dy
    if 0 <= NX < H and 0 <= NY < W:
      CELL = A_LIST[NX][NY]
      if CELL == '#':
        continue
      if CELL == 'x' and SWITCH_STATE == 0:
        continue
      if CELL == 'o' and SWITCH_STATE == 1:
        continue
      NEW_SWITCH_STATE = SWITCH_STATE
      if CELL == '?':
        NEW_SWITCH_STATE = 1 - SWITCH_STATE
      if (NX, NY, NEW_SWITCH_STATE) not in VISITED:
        VISITED.add((NX, NY, NEW_SWITCH_STATE))
        QUEUE.append((NX, NY, NEW_SWITCH_STATE, DIST + 1))

print(-1)