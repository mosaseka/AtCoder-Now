H, W, N = map(int, input().split())
LIST = [[False] * W for _ in range(H)]
for _ in range(N):
  X, Y = map(int, input().split())
  LIST[X - 1][Y - 1] = True

Q = int(input())
for _ in range(Q):
  QUERY = list(map(int, input().split()))
  if QUERY[0] == 1:
    X = QUERY[1] - 1
    COUNT = sum(LIST[X])
    print(COUNT)
    for j in range(W):
      LIST[X][j] = False
  else:
    Y = QUERY[1] - 1
    COUNT = sum(LIST[i][Y] for i in range(H))
    print(COUNT)
    for i in range(H):
      LIST[i][Y] = False