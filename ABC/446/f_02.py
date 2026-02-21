import heapq

N, M = map(int, input().split())

G = [[] for _ in range(N)]
for _ in range(M):
  U, V = map(int, input().split())
  G[U-1].append(V-1)

USED = [False] * N
USED[0] = True

PQ = [0]

ANSWER = [-1] * N

S_PQ = []
while PQ:
  X = heapq.heappop(PQ)
  heapq.heappush(S_PQ, -X)
  for to in G[X]:
    if USED[to]:
      continue
    USED[to] = True
    heapq.heappush(PQ, to)
  
  TOP = -S_PQ[0]
  if TOP == len(S_PQ) - 1:
    ANSWER[TOP] = len(PQ)

for i in range(N):
  print(ANSWER[i])