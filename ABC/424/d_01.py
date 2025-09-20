T = int(input())

for t in range(T):
  H, W = map(int, input().split())
  S = [list(map(str,input())) for j in range(H)]
  COUNT = 0
  for i in range(H - 1):
    for j in range(W - 1):
      if (S[i][j] == '#' and S[i][j+1] == '#' and S[i+1][j] == '#' and S[i+1][j+1] == '#'):
        S[i+1][j+1] = '.' # Greedy
        COUNT += 1
  print(COUNT)