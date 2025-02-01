N, M = map(int, input().split())
S_LIST = [str(input()) for i in range(N)]
T_LIST = [str(input()) for i in range(M)]

for a in range(N - M + 1):
  for b in range(N - M + 1):
    FLAG = False
    for i in range(M):
      for j in range(M):
        if S_LIST[a + i][b + j] != T_LIST[i][j]:
          FLAG = True
          break
      if FLAG:
        break
    if not FLAG:
      print(a + 1, b + 1)
      exit()