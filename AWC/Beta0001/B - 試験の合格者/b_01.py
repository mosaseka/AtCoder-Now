N, L, R = map(int, input().split())
P_LIST = list(map(int, input().split()))

MAX_INDEX = -1
MAX_SCORE = -1000000000

for i in range(N):
  if L <= P_LIST[i] <= R:
    if P_LIST[i] > MAX_SCORE:
      MAX_SCORE = P_LIST[i]
      MAX_INDEX = i + 1

if MAX_INDEX == -1:
  print(-1)
else:
  print(MAX_INDEX)