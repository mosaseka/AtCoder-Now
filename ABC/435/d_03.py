from collections import deque

N, M = map(int, input().split())
XY_LIST = [tuple(map(int, input().split())) for i in range(M)]
Q = int(input())
REVERSE_GRAPH = [[] for i in range(N + 1)]
CAN_REACH = [False] * (N + 1)

for x, y in XY_LIST:
  REVERSE_GRAPH[y].append(x)

for i in range(Q):
  QUERY = list(map(int, input().split()))
  if QUERY[0] == 1:
    v = QUERY[1]
    if CAN_REACH[v]:
      continue
    QUEUE = deque([v])
    CAN_REACH[v] = True
    while QUEUE:
      NODE = QUEUE.popleft()
      for prev in REVERSE_GRAPH[NODE]:
        if not CAN_REACH[prev]:
          CAN_REACH[prev] = True
          QUEUE.append(prev)
  else:
    if CAN_REACH[QUERY[1]]:
      print("Yes")
    else:
      print("No")