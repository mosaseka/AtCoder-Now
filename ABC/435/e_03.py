import bisect

N, Q = map(int, input().split())
BLACK = []
TOTAL = 0

for i in range(Q):
  L, R = map(int, input().split())
  LEFT_INDEX = bisect.bisect_left(BLACK, (L, -1))
  START_INDEX = LEFT_INDEX
  END_INDEX = LEFT_INDEX
  NEW_L = L
  NEW_R = R
  if START_INDEX > 0 and BLACK[START_INDEX - 1][1] >= L - 1:
    START_INDEX -= 1
    TOTAL -= (BLACK[START_INDEX][1] - BLACK[START_INDEX][0] + 1)
    NEW_L = min(NEW_L, BLACK[START_INDEX][0])
    NEW_R = max(NEW_R, BLACK[START_INDEX][1])
  while END_INDEX < len(BLACK) and BLACK[END_INDEX][0] <= R + 1:
    TOTAL -= (BLACK[END_INDEX][1] - BLACK[END_INDEX][0] + 1)
    NEW_L = min(NEW_L, BLACK[END_INDEX][0])
    NEW_R = max(NEW_R, BLACK[END_INDEX][1])
    END_INDEX += 1
  TOTAL += (NEW_R - NEW_L + 1)
  BLACK[START_INDEX:END_INDEX] = [(NEW_L, NEW_R)]
  print(N - TOTAL)