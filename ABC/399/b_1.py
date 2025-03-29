N = int(input())
P_LIST = list(map(int, input().split()))
LIST = []

for i in range(N):
  LIST.append([P_LIST[i], i + 1, 0])

LIST.sort(reverse=True, key=lambda x: x[0])

r = 1
for i in range(N):
  if i > 0 and LIST[i][0] != LIST[i - 1][0]:
    r = i + 1
  LIST[i][2] = r
LIST.sort(key=lambda x: x[1])

for i in range(N):
  print(LIST[i][2])