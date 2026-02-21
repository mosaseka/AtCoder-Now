from collections import deque

N, M = map(int, input().split())
UV_LIST = [tuple(map(int, input().split())) for _ in range(M)]

GRAPH = [[] for _ in range(N+1)]
for u, v in UV_LIST:
  GRAPH[u].append(v)

for i in range(1, N+1):
  VISITED_INSIDE = [False] * (N+1)
  CHECK = deque([1])
  VISITED_INSIDE[1] = True

  while CHECK:
    NODE = CHECK.popleft()
    for next in GRAPH[NODE]:
      if next <= i and not VISITED_INSIDE[next]:
        CHECK.append(next)
        VISITED_INSIDE[next] = True
  
  POSSIBLE = all(VISITED_INSIDE[j] for j in range(1, i+1))
  if not POSSIBLE:
    print(-1)
    continue

  NEED_DELETE = set()
  for j in range(1, i+1):
    for next in GRAPH[j]:
      if next > i:
        NEED_DELETE.add(next)

  print(len(NEED_DELETE))