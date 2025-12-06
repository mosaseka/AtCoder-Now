from collections import deque

def DFS_REVERSE(GRAPH, START, SET):
  QUEUE = deque([START])
  VISITED = [False] * len(GRAPH)
  VISITED[START] = True
  while QUEUE:
    NODE = QUEUE.popleft()
    SET.add(NODE)
    for i in GRAPH[NODE]:
      if not VISITED[i]:
        VISITED[i] = True
        QUEUE.append(i)


N, M = map(int, input().split())
XY_LIST = [tuple(map(int, input().split())) for i in range(M)]
Q = int(input())
REVERSE_GRAPH = [[] for i in range(N + 1)]
BLACK = set()

for x, y in XY_LIST:
  REVERSE_GRAPH[y].append(x)

for i in range(Q):
  QUERY = list(map(int, input().split()))
  match QUERY[0]:
    case 1:
      BLACK.add(QUERY[1])
      DFS_REVERSE(REVERSE_GRAPH, QUERY[1], BLACK)
    case 2:
      if QUERY[1] in BLACK:
        print("Yes")
      else:
        print("No")