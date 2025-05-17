H, W, N = map(int, input().split())
ROW_POINTS = [set() for _ in range(H)]
COL_POINTS = [set() for _ in range(W)]

for _ in range(N):
  X, Y = map(int, input().split())
  X -= 1
  Y -= 1
  if Y not in ROW_POINTS[X]:
    ROW_POINTS[X].add(Y)
    COL_POINTS[Y].add(X)

Q = int(input())
for _ in range(Q):
  QUERY = list(map(int, input().split()))
  if QUERY[0] == 1:
    X = QUERY[1] - 1
    print(len(ROW_POINTS[X]))
    for Y in ROW_POINTS[X]:
      COL_POINTS[Y].remove(X)
    ROW_POINTS[X].clear()
  else:
    Y = QUERY[1] - 1
    print(len(COL_POINTS[Y]))
    for X in COL_POINTS[Y]:
      ROW_POINTS[X].remove(Y)
    COL_POINTS[Y].clear()