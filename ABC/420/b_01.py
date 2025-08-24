N, M = map(int, input().split())
S = [str(input()) for _ in range(N)]
POINT = [0] * N
ZERO = 0
ZERO_LIST = []
ONE = 0
ONE_LIST = []

for i in range(M):
  ZERO = 0
  ZERO_LIST = []
  ONE = 0
  ONE_LIST = []
  for j in range(N):
    if S[j][i] == "0":
      ZERO += 1
      ZERO_LIST.append(j)
    else:
      ONE += 1
      ONE_LIST.append(j)
  if ZERO < ONE:
    for k in ZERO_LIST:
      POINT[k] += 1
  elif ONE < ZERO:
    for k in ONE_LIST:
      POINT[k] += 1
  else:
    pass

MAX = max(POINT)
LIST = [i + 1 for i, point in enumerate(POINT) if point == MAX]
print(" ".join(map(str, LIST)))