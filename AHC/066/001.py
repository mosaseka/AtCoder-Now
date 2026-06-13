from collections import deque

N, M, T = map(int, input().split())
V = [input().strip() for _ in range(N)]
H = [input().strip() for _ in range(N-1)]

BALLS = []
BASKETS = []
for i in range(M):
  B, C, D, E = map(int, input().split())
  BALLS.append((B, C))
  BASKETS.append((D, E))

DI = [0, 1, 0, -1]
DJ = [1, 0, -1, 0]

def CAN(i, j, nd):
  match nd:
    case 0:
      return j+1 < N and V[i][j] == "0"
    case 1:
      return i+1 < N and H[i][j] == "0"
    case 2:
      return j-1 >= 0 and V[i][j-1] == "0"
    case _:
      return i-1 >= 0 and H[i-1][j] == "0"

def BFS(start, goal):
  if start == goal:
    return []
  
  NOW = [[None] * N for _ in range(N)]
  DEQ = deque([start])
  NOW[start[0]][start[1]] = (-1, -1, -1)

  while DEQ:
    i, j = DEQ.popleft()
    for nd in range(4):
      if not CAN(i, j, nd):
        continue
      ni, nj = i + DI[nd], j + DJ[nd]
      if NOW[ni][nj] is not None:
        continue
      NOW[ni][nj] = (i, j, nd)
      if (ni, nj) == goal:
        DEQ.clear()
        break
      DEQ.append((ni, nj))
  
  PATH = []
  ci, cj = goal
  while (ci, cj) != start:
    pi, pj, nd = NOW[ci][cj]
    PATH.append(nd)
    ci, cj = pi, pj
  
  PATH.reverse()
  return PATH

def TURN(now, next):
  DIFF = (next - now) % 4
  match DIFF:
    case 0:
      return ""
    case 1:
      return "R"
    case 2:
      return "RR"
    case _:
      return "L"

def MOVE(path, now):
  LIST = []
  d = now
  for nd in path:
    LIST.append(TURN(d, nd))
    LIST.append("F")
    d = nd
  return "".join(LIST), d

def ROUTE(position, direction, goal):
  path = BFS(position, goal)
  ops, ndirection = MOVE(path, direction)
  return ops, goal, ndirection

POSITION = (0, 0)
DIRECTION = 0
USED = [False] * M
ANSWER = []

while True:
  BEST = None

  for k in range(M):
    if USED[k]:
      continue

    ops1, pos1, dir1 = ROUTE(POSITION, DIRECTION, BALLS[k])
    ops2, pos2, dir2 = ROUTE(pos1, dir1, BASKETS[k])
    ops = ops1 + "S" + ops2 + "S"

    if len(ANSWER) + len(ops) > T:
      continue

    if BEST is None or len(ops) < len(BEST[0]):
      BEST = (ops, pos2, dir2, k)
    
  
  if BEST is None:
    break

  ops, POSITION, DIRECTION, idx = BEST
  ANSWER.extend(ops)
  USED[idx] = True

ANSWER = ANSWER[:T]

if ANSWER:
  print("\n".join(ANSWER))
