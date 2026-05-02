from collections import deque

T = int(input())

for _ in range(T):
  N, M = map(int, input().split())
  
  CHECK = [[] for _ in range(N)]

  for _ in range(M):
    U, V = map(int, input().split())
    U, V = U-1, V-1
    CHECK[U].append(V)
    CHECK[V].append(U)
  
  for i in range(N):
    CHECK[i].append(i)
  
  W = int(input())
  S = [str(input()) for _ in range(N)]

  GOOD = [bytearray(N) for _ in range(W)]
  for i in range(N):
    for d in range(W):
      if S[i][d] == "o":
        GOOD[d][i] = 1
  
  COUNT = [[0] * N for _ in range(W)]
  DEQ = deque()

  for d in range(W):
    nd = (d+1) % W
    for u in range(N):
      if not GOOD[d][u]:
        continue

      c = 0
      for v in CHECK[u]:
        if GOOD[nd][v]:
          c += 1
      
      COUNT[d][u] = c
      if c == 0:
        GOOD[d][u] = 0
        DEQ.append((d, u))
  
  while DEQ:
    d, u = DEQ.popleft()
    pd = (d-1) % W

    for p in CHECK[u]:
      if not GOOD[pd][p]:
        continue

      COUNT[pd][p] -= 1
      if COUNT[pd][p] == 0:
        GOOD[pd][p] = 0
        DEQ.append((pd, p))
  
  if any(GOOD[0]):
    print("Yes")
  else:
    print("No")