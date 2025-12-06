from sortedcontainers import SortedList

N, Q = map(int, input().split())
BLACK = SortedList()
BLACK_TOTAL = 0

for i in range(Q):
  L, R = map(int, input().split())
  INDEX = BLACK.bisect_left((L, 0))
  if INDEX > 0 and BLACK[INDEX - 1][1] >= L - 1:
    INDEX -= 1
  NEW_L = L
  NEW_R = R
  REMOVED_COUNT = 0
  START = INDEX
  while INDEX < len(BLACK) and BLACK[INDEX][0] <= NEW_R + 1:
    REMOVED_COUNT += BLACK[INDEX][1] - BLACK[INDEX][0] + 1
    NEW_L = min(NEW_L, BLACK[INDEX][0])
    NEW_R = max(NEW_R, BLACK[INDEX][1])
    INDEX += 1
  BLACK_TOTAL = BLACK_TOTAL - REMOVED_COUNT + (NEW_R - NEW_L + 1)
  del BLACK[START:INDEX]
  BLACK.add((NEW_L, NEW_R))
  print(N - BLACK_TOTAL)