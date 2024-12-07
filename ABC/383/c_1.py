from collections import deque

def REACHABLE(H, W, D, S_LIST):
  VECTOR = [(-1, 0), (1, 0), (0, -1), (0, 1)]
  REACHABLE_LIST = [[False] * W for _ in range(H)]

  def BFS(X_START, Y_START):
    QUEUE = deque([[X_START, Y_START, 0]])
    VISITED = [[False] * W for _ in range(H)]
    VISITED[X_START][Y_START] = True
    REACHABLE_LIST[X_START][Y_START] = True

    while QUEUE:
      X, Y, DIST = QUEUE.popleft()
      if DIST >= D:
        continue
      for DX, DY in VECTOR:
        NX, NY = X + DX, Y + DY
        if 0 <= NX < H and 0 <= NY < W and not VISITED[NX][NY] and S_LIST[NX][NY] != "#":
          VISITED[NX][NY] = True
          REACHABLE_LIST[NX][NY] = True
          QUEUE.append([NX, NY, DIST + 1])

  for i in range(H):
    for j in range(W):
      if S_LIST[i][j] == "H":
        BFS(i, j)

  return REACHABLE_LIST

# 入力の読み込み
H, W, D = map(int, input().split())
S_LIST = [list(input()) for _ in range(H)]
REACHABLE_LIST = REACHABLE(H, W, D, S_LIST)
COUNT = 0

#print(REACHABLE_LIST)

for i in range(H):
  for j in range(W):
    if REACHABLE_LIST[i][j]:
      COUNT += 1

print(COUNT)