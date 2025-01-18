from collections import deque 

Q = int(input())
DEQ = deque()
QUERY = []
INDEX = 0
LK = 0
SUM = 0
MINUS = 0

for i in range(Q):
  QUERY = list(map(int, input().split()))
  if QUERY[0] == 2:
    INDEX = QUERY[0]
  else:
    INDEX = QUERY[0]
    LK = QUERY[1]
  if INDEX == 1:
    DEQ.append([LK, SUM])
    SUM += LK
  elif INDEX == 2:
    MINUS += DEQ[0][0]
    DEQ.popleft()
  elif INDEX == 3:
    print(DEQ[LK-1][1] - MINUS)