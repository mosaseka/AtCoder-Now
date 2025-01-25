H,W = map(int,input().split())
S = [list(input()) for _ in range(H)]
ABLE = set()
MIN_X = 10000
MIN_Y = 10000
MAX_X = 0
MAX_Y = 0

for i in range(H):
  for j in range(W):
    if S[i][j] == "?":
      ABLE.add((i,j))
    elif S[i][j] == "#":
      MIN_X = min(MIN_X,j)
      MIN_Y = min(MIN_Y,i)
      MAX_X = max(MAX_X,j)
      MAX_Y = max(MAX_Y,i)

#print(ABLE)

for i in range(MIN_Y, MAX_Y+1):
  for j in range(MIN_X, MAX_X+1):
    if (i,j) in ABLE:
      pass
    elif S[i][j] == "#":
      pass
    else:
      print("No")
      exit()

print("Yes")