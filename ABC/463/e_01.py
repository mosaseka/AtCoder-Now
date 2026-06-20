import heapq

N, M, Y = map(int, input().split())

GRAPH = [[] for _ in range(N)]
for _ in range(M):
  U, V, T = map(int, input().split())
  U -= 1
  V -= 1
  GRAPH[U].append((V, T))
  GRAPH[V].append((U, T))

X_LIST = list(map(int, input().split()))

GATE = N
DIST = [float('inf')] * (N + 1)
DIST[0] = 0
PQ = [(0, 0)]

while PQ:
  CURRENT_DIST, VERTEX = heapq.heappop(PQ)

  if CURRENT_DIST != DIST[VERTEX]:
    continue

  if VERTEX == GATE:
    for NEXT_VERTEX, X in enumerate(X_LIST):
      NEXT_DIST = CURRENT_DIST + X
      if NEXT_DIST < DIST[NEXT_VERTEX]:
        DIST[NEXT_VERTEX] = NEXT_DIST
        heapq.heappush(PQ, (NEXT_DIST, NEXT_VERTEX))
    continue

  NEXT_DIST = CURRENT_DIST + X_LIST[VERTEX] + Y
  if NEXT_DIST < DIST[GATE]:
    DIST[GATE] = NEXT_DIST
    heapq.heappush(PQ, (NEXT_DIST, GATE))

  for NEXT_VERTEX, T in GRAPH[VERTEX]:
    NEXT_DIST = CURRENT_DIST + T
    if NEXT_DIST < DIST[NEXT_VERTEX]:
      DIST[NEXT_VERTEX] = NEXT_DIST
      heapq.heappush(PQ, (NEXT_DIST, NEXT_VERTEX))

print(*DIST[1:N])