def CanCover(X, M, MAX_TOTAL_STRENGTH):
  N = len(X)
  i = 0
  CNT = 0
  USED = 0.0
  while i < N:
    REMAIN = MAX_TOTAL_STRENGTH - USED
    if CNT == M or REMAIN < 0:
      return False
    MAX_LEN = REMAIN
    CENTER = X[i] + MAX_LEN / 2
    REACH = CENTER + MAX_LEN / 2
    j = i
    while j < N and X[j] <= REACH:
      j += 1
    USED += X[j - 1] - X[i]
    CNT += 1
    i = j
  return True

N, M = map(int, input().split())
X = list(map(int, input().split()))
X.sort()

LEFT = 0.0
RIGHT = 1e15
ANSWER = RIGHT

for _ in range(100):
  MID = (LEFT + RIGHT) / 2
  if CanCover(X, M, MID):
    ANSWER = MID
    RIGHT = MID
  else:
    LEFT = MID

print(f"{ANSWER:.10f}")