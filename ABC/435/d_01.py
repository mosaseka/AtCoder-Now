from collections import deque

def DFS(GRAPH, START, SET):
  CHECK = [False] * len(GRAPH)
  DEQUE = deque([START])
  while DEQUE:
    NODE = DEQUE.pop()
    if CHECK[NODE]:
      continue
    CHECK[NODE] = True
    if NODE in SET:
      return True
    for i in GRAPH[NODE]:
      if not CHECK[i]:
        DEQUE.append(i)
  return False

N, M = map(int, input().split())
XY_LIST = [tuple(map(int, input().split())) for i in range(M)]
Q = int(input())
GRAPH = [[] for i in range(N + 1)]
BLACK = set()

for x, y in XY_LIST:
  GRAPH[x].append(y)

for i in range(Q):
  QUERY = list(map(int, input().split()))
  match QUERY[0]:
    case 1:
      BLACK.add(QUERY[1])
    case 2:
      if DFS(GRAPH, QUERY[1], BLACK):
        print("Yes")
      else:
        print("No")