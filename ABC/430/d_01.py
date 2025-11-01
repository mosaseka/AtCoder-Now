import bisect

N = int(input())
X_LIST = list(map(int, input().split()))
POSITIONS = [0]

for i in range(N):
  NEW_VAL = X_LIST[i]
  POS = bisect.bisect_left(POSITIONS, NEW_VAL)
  POSITIONS.insert(POS, NEW_VAL)
  
  ANSWER = 0
  for j in range(len(POSITIONS)):
    MIN_DIST = float('inf')
    if j > 0:
      MIN_DIST = min(MIN_DIST, POSITIONS[j] - POSITIONS[j - 1])
    if j < len(POSITIONS) - 1:
      MIN_DIST = min(MIN_DIST, POSITIONS[j + 1] - POSITIONS[j])
    ANSWER += MIN_DIST
  
  print(ANSWER)