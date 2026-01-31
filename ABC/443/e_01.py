T = int(input())

for _ in range(T):
  N, C = map(int, input().split())
  S_LIST = [list(input().strip()) for i in range(N)]

  C -= 1
  LOW = [-1] * N
  for i in range(N):
    for j in range(N):
      if S_LIST[i][j] == "#":
        LOW[j] = i
  
  DP = [[0] * N for i in range(N)]
  for i in range(N):
    DP[i][C] = 1

  for i in range(N-2, -1, -1):
    for j in range(N):
      if DP[i][j] > 0:
        continue
      FLAG = False
      if DP[i+1][j] > 0:
        FLAG = True
      if j > 0 and DP[i+1][j-1] > 0:
        FLAG = True
      if j+1 < N and DP[i+1][j+1] > 0:
        FLAG = True
      if FLAG:
        if S_LIST[i][j] == ".":
          DP[i][j] = 1
        else:
          if LOW[j] == i:
            for k in range(0, i+1):
              DP[k][j] = 1
  
  print(''.join(str(x) for x in DP[0]))