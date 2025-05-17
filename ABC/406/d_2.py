H, W, N = map(int, input().split())
POINTS = set()
ROW_COUNT = [0] * H
COL_COUNT = [0] * W

for _ in range(N):
  X, Y = map(int, input().split())
  X -= 1
  Y -= 1
  if (X, Y) not in POINTS:
    POINTS.add((X, Y))
    ROW_COUNT[X] += 1
    COL_COUNT[Y] += 1

Q = int(input())

for _ in range(Q):
  QUERY = list(map(int, input().split()))
  if QUERY[0] == 1:
    X = QUERY[1] - 1
    print(ROW_COUNT[X])
    for Y in range(W):
      if (X, Y) in POINTS:
        POINTS.remove((X, Y))
        ROW_COUNT[X] -= 1
        COL_COUNT[Y] -= 1
  else:
    Y = QUERY[1] - 1
    print(COL_COUNT[Y])
    for X in range(H):
      if (X, Y) in POINTS:
        POINTS.remove((X, Y))
        ROW_COUNT[X] -= 1
        COL_COUNT[Y] -= 1