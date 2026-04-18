from collections import deque

N, M = map(int, input().split())

GRAPH = [[] for _ in range(N + 1)]

for i in range(M):
  A, B = map(int, input().split())
  GRAPH[A].append(B)

VISITED = [False] * (N + 1)
DEQ = deque([1])
VISITED[1] = True
ANSWER = 1

while DEQ:
  CHECK = DEQ.pop()
  for i in GRAPH[CHECK]:
    if not VISITED[i]:
      DEQ.append(i)
      VISITED[i] = True
      ANSWER += 1

print(ANSWER)