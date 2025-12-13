from collections import deque, defaultdict

H, W = map(int, input().split())
S = [list(map(str, input())) for i in range(H)]

WARP = defaultdict(list)
for i in range(H):
  for j in range(W):
    if S[i][j] not in {".", "#"}:
      WARP[S[i][j]].append((i, j))

# BFS & DP
DP = [[float("inf")] * W for i in range(H)]
QUEUE = deque([(0, 0, 0)])
DP[0][0] = 0
VISITED_WARP = set()

while QUEUE:
  ROW, COL, COST = QUEUE.popleft()
  if COST > DP[ROW][COL]:
    continue
  for D_ROW, D_COL in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
    N_ROW = ROW + D_ROW
    N_COL = COL + D_COL
    if 0 <= N_ROW < H and 0 <= N_COL < W and S[N_ROW][N_COL] != "#":
      if DP[N_ROW][N_COL] > COST + 1:
        DP[N_ROW][N_COL] = COST + 1
        QUEUE.append((N_ROW, N_COL, COST + 1))
  if S[ROW][COL] not in {".", "#"}:
    CHAR = S[ROW][COL]
    if (ROW, COL) not in VISITED_WARP:
      VISITED_WARP.add((ROW, COL))
      for N_ROW, N_COL in WARP[CHAR]:
        if (N_ROW, N_COL) != (ROW, COL) and DP[N_ROW][N_COL] > COST + 1:
          DP[N_ROW][N_COL] = COST + 1
          QUEUE.append((N_ROW, N_COL, COST + 1))

if DP[H-1][W-1] == float("inf"):
  print(-1)
else:
  print(DP[H-1][W-1])