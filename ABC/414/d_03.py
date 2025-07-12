def CanCover(X, M, TOTAL_STRENGTH):
  N = len(X)
  i = 0
  CNT = 0
  USED = 0

  while i < N:
    REMAIN = TOTAL_STRENGTH - USED
    if CNT == M or REMAIN < 0:
      return False

    LEFT = i
    RIGHT = N
    R = REMAIN
    REACH = X[i] + R
    j = i
    while j < N and X[j] <= REACH:
      j += 1
    if j == i:
      return False

    USED += X[j - 1] - X[i]
    CNT += 1
    i = j

  return True

N, M = map(int, input().split())
X = list(map(int, input().split()))
X.sort()

LEFT = 0
RIGHT = 10**15
ANSWER = RIGHT

while LEFT <= RIGHT:
  MID = (LEFT + RIGHT) // 2
  if CanCover(X, M, MID):
    ANSWER = MID
    RIGHT = MID - 1
  else:
    LEFT = MID + 1

print(ANSWER)