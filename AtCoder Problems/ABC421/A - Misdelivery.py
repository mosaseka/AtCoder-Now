N = int(input())
S_LIST = [str(input()) for i in range(N)]
X, Y = map(str, input().split())
X = int(X)

if S_LIST[X-1] == Y:
  print("Yes")
else:
  print("No")