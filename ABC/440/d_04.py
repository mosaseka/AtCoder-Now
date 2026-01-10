from bisect import bisect_left, bisect_right

N, Q = map(int, input().split())
A_LIST = list(map(int, input().split()))
XY_LIST = [list(map(int, input().split())) for _ in range(Q)]

A_LIST.sort()

GAP_LIST = [A_LIST[i+1] - A_LIST[i] - 1 for i in range(N-1)]
SUM_LIST = [0] * N
SUM = 0

for i, g in enumerate(GAP_LIST):
  SUM += g
  SUM_LIST[i+1] = SUM

FINAL = A_LIST[-1]
ANSWER = []

for X, Y in XY_LIST:
  INDEX = bisect_left(A_LIST, X)

  if INDEX == N:
    ANSWER.append(str(X + Y - 1))
    continue

  INIT = A_LIST[INDEX] - X
  if Y <= INIT:
    ANSWER.append(str(X + Y - 1))
    continue

  Y -= INIT

  if INDEX == N - 1:
    ANSWER.append(str(A_LIST[-1] + Y))
    continue

  BASE = SUM_LIST[INDEX]
  TARGET = BASE + Y
  
  CHECK = bisect_left(SUM_LIST, TARGET, INDEX + 1)
  if CHECK == N:
    MISSING = SUM_LIST[N-1] - BASE
    ANSWER.append(str(A_LIST[-1] + (Y - MISSING)))
  else:
    GAP = CHECK - 1
    PAST = SUM_LIST[GAP] - BASE
    ANSWER.append(str(A_LIST[GAP] + (Y - PAST)))

for i in ANSWER:
  print(i)