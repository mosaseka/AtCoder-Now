import bisect

def CanCover(X, M, TOTAL_STRENGTH):
  N = len(X)
  i = 0
  USED = 0
  CNT = 0

  while i < N:
    MAX_R = TOTAL_STRENGTH - USED
    if CNT >= M or MAX_R < 0:
      return False

    RIGHT = X[i] + MAX_R
    j = bisect.bisect_right(X, RIGHT)
    if j == i:
      return False

    USED += X[j - 1] - X[i]
    CNT += 1
    i = j

  return CNT <= M and USED <= TOTAL_STRENGTH

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