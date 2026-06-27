N, M = map(int, input().split())

COUNT = [0] * (N+1)
EVENTS = [[] for _ in range(M+1)]

for _ in range(N):
  A, D, B = map(int, input().split())

  COUNT[A] += 1

  if A != B:
    EVENTS[D].append((A, B))

ANSWER = 0

for i in range(1, N+1):
  if COUNT[i] > 0:
    ANSWER += 1

for i in range(1, M+1):
  for a, b in EVENTS[i]:
    COUNT[a] -= 1

    if COUNT[a] == 0:
      ANSWER -= 1
    if COUNT[b] == 0:
      ANSWER += 1
    
    COUNT[b] += 1
  
  print(ANSWER)