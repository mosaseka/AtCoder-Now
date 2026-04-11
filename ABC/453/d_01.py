from collections import deque

def STATE(X, Y, D):
  return ((Y * W + X) << 2 | D)

H, W = map(int, input().split())
S_LIST = [list(map(str, input())) for _ in range(H)]

MOVE = [[1, 0], [-1, 0], [0, 1], [0, -1]]
MOVE2 = ["R", "L", "D", "U"]

SX, SY = -1, -1
GX, GY = -1, -1

for y in range(H):
  for x in range(W):
    if S_LIST[y][x] == "S":
      SX = x
      SY = y
    elif S_LIST[y][x] == "G":
      GX = x
      GY = y

N = 4 * H * W
VISITED = [False] * N
PARENT = [-1] * N
LAST = [""] * N
DEQ = deque()

for d, (dx, dy) in enumerate(MOVE):
  nx = SX + dx
  ny = SY + dy
  if (0 <= nx < W) and (0 <= ny < H) and S_LIST[ny][nx] != "#":
    CHECK = STATE(nx, ny, d)
    VISITED[CHECK] = True
    PARENT[CHECK] = -2
    LAST[CHECK] = MOVE2[d]
    DEQ.append(CHECK)

GOAL = -1

while DEQ:
  NOW = DEQ.popleft()
  POSITION = NOW >> 2
  D = NOW & 3
  X = POSITION % W
  Y = POSITION // W

  if S_LIST[Y][X] == "G":
    GOAL = NOW
    break

  for nd, (dx, dy) in enumerate(MOVE):
    if S_LIST[Y][X] == "o" and nd != D:
      continue
    if S_LIST[Y][X] == "x" and nd == D:
      continue

    nx = X + dx
    ny = Y + dy
    if not (0 <= nx < W and 0 <= ny < H):
      continue
    if S_LIST[ny][nx] == "#":
      continue

    ns = STATE(nx, ny, nd)
    if VISITED[ns]:
      continue

    VISITED[ns] = True
    PARENT[ns] = NOW
    LAST[ns] = MOVE2[nd]
    DEQ.append(ns)

    if S_LIST[ny][nx] == "G":
      GOAL = ns
      DEQ.clear()
      break

if GOAL == -1:
  print("No")
else:
  ANSWER = []
  NOW = GOAL

  while True:
    ANSWER.append(LAST[NOW])
    if PARENT[NOW] == -2:
      break
    NOW = PARENT[NOW]
  
  ANSWER.reverse()
  print("Yes")
  print("".join(ANSWER))