import heapq

N, M = map(int, input().split())
G = [[] for _ in range(N + 1)]
S = ""
SAFE = []
DANGER = []
INF = 10**18
BEST = [[(INF, -1), (INF, -1)] for i in range(N + 1)]
PQ = []
OUT = []

for i in range(M):
  U, VERTEX = map(int, input().split())
  G[U].append(VERTEX)
  G[VERTEX].append(U)

S = str(input())

for i, j in enumerate(S, start=1):
  if j == 'S':
    SAFE.append(i)
  else:
    DANGER.append(i)

for i in SAFE:
  BEST[i][0] = (0, i)
  heapq.heappush(PQ, (0, i, i))

def Dijkstra(VERTEX, CHECK):
  D, START = CHECK
  B0, B1 = BEST[VERTEX]
  if START == B0[1]:
    if D < B0[0]:
      BEST[VERTEX][0] = (D, START)
      return True
    return False
  if START == B1[1]:
    if D < B1[0]:
      BEST[VERTEX][1] = (D, START)
      if BEST[VERTEX][1][0] < BEST[VERTEX][0][0]:
        BEST[VERTEX][0], BEST[VERTEX][1] = BEST[VERTEX][1], BEST[VERTEX][0]
      return True
    return False
  if D < B0[0]:
    BEST[VERTEX][1] = B0
    BEST[VERTEX][0] = (D, START)
    return True
  if D < B1[0]:
    BEST[VERTEX][1] = (D, START)
    return True
  return False

while PQ:
  DIST, VERTEX, START = heapq.heappop(PQ)
  if not ((BEST[VERTEX][0][1] == START and BEST[VERTEX][0][0] == DIST) or
          (BEST[VERTEX][1][1] == START and BEST[VERTEX][1][0] == DIST)):
    continue
  ND = DIST + 1
  for i in G[VERTEX]:
    if Dijkstra(i, (ND, START)):
      heapq.heappush(PQ, (ND, i, START))

for i in DANGER:
  D1, S1 = BEST[i][0]
  D2, S2 = BEST[i][1]
  OUT.append(str(D1 + D2))

for i in OUT:
  print(i)