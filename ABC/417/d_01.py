N = int(input())
PAB_LIST = [list(map(int, input().split())) for _ in range(N)]
Q = int(input())

for i in range(Q):
  X = int(input())
  for j in range(N):
    if X <= PAB_LIST[j][0]:
      X += PAB_LIST[j][1]
    else:
      X -= PAB_LIST[j][2]
      if X < 0:
        X = 0
  print(X)