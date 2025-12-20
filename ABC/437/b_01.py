H, W, N = map(int, input().split())
A_LIST = [list(map(int, input().split())) for i in range(H)]
COUNT_LIST = [0] * H

for i in range(N):
  B = int(input())
  for j in range(H):
    for k in range(W):
      if A_LIST[j][k] == B:
        COUNT_LIST[j] += 1

print(max(COUNT_LIST))