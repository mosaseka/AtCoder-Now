from collections import deque

Q = int(input())
DEQ = deque()

for i in range(Q):
  QUERY = list(map(int, input().split()))
  if QUERY[0] == 1:
    DEQ.append(QUERY[1])
  elif QUERY[0] == 2:
    print(DEQ.popleft())