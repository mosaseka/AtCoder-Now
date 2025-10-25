import heapq
from collections import defaultdict

def Dijkstra(START):
  DIST = [float("inf")] * (N + 1)
  DIST[START] = 0
  CHECK = [(0, START)]
  while CHECK:
    COST, NODE = heapq.heappop(CHECK)
    if COST > DIST[NODE]:
      continue
    for i in GRAPH[NODE]:
      if DIST[NODE] + 1 < DIST[i]:
        DIST[i] = DIST[NODE] + 1
        heapq.heappush(CHECK, (DIST[i], i))
  return DIST

N, M = map(int, input().split())
UV_LIST = [tuple(map(int, input().split())) for i in range(M)]
S = str(input())
SAFE = []
DANGER = []

GRAPH = defaultdict(list)
for u, v in UV_LIST:
  GRAPH[u].append(v)
  GRAPH[v].append(u)

for i in range(N):
  if S[i] == "S":
    SAFE.append(i+1)
  else:
    DANGER.append(i+1)

for i in DANGER:
  DIST = Dijkstra(i)
  DISTANCES = []
  for j in SAFE:
    DISTANCES.append(DIST[j])
    
  DISTANCES.sort()
  print(DISTANCES[0] + DISTANCES[1])