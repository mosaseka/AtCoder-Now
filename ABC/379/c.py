N, M = map(int, input().split())
X_LIST = list(map(int, input().split()))
A_LIST = list(map(int, input().split()))
LIST = []
NUM = 0
INDEX = 0

for i in range(M):
  LIST.append([X_LIST[i], A_LIST[i]])

LIST.sort()

for i in range(M):
  if NUM < LIST[i][0] - 1:
    print(-1)
    exit()
  else:
    NUM += LIST[i][1]
    INDEX += LIST[i][1] * LIST[i][0]

if NUM != N:
  print(-1)
else:
  print(N *(N+1) //2 - INDEX)