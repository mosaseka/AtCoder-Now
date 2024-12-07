from itertools import combinations

H,W,D = map(int, input().split())
S_LIST = [list(map(str,input())) for i in range(H)]
CHECK = []
COMB = []
COUNT = 0
COUNT_LIST = []

for i in range(H):
  for j in range(W):
    if S_LIST[i][j] == ".":
      CHECK.append([i,j])

COMB = list(combinations(CHECK,2))
#print(COMB)

for i in range(len(COMB)):
  COUNT = 0
  for j in range(H):
    for k in range(W):
      if S_LIST[j][k] == ".":
        if abs(COMB[i][0][0]-j) + abs(COMB[i][0][1]-k) <= D or abs(COMB[i][1][0]-j) + abs(COMB[i][1][1]-k) <= D:
          COUNT += 1
  COUNT_LIST.append(COUNT)

#print(COUNT_LIST)
print(max(COUNT_LIST))