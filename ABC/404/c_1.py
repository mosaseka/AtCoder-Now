from collections import defaultdict, deque

def is_cycle_graph(N, M, EDGES):
  if M != N:
    return False
  
  G = defaultdict(list)
  
  for u, v in EDGES:
    G[u].append(v)
    G[v].append(u)

  for NODE in range(1, N + 1):
    if len(G[NODE]) != 2:
      return False
    
  VISITED = set()
  QUEUE = deque([1])
  VISITED.add(1)

  while QUEUE:
    NOW = QUEUE.popleft()
    for NEIGHBOR in G[NOW]:
      if NEIGHBOR not in VISITED:
        VISITED.add(NEIGHBOR)
        QUEUE.append(NEIGHBOR)

  return len(VISITED) == N

N, M = map(int, input().split())
EDGES = [tuple(map(int, input().split())) for _ in range(M)]

if is_cycle_graph(N, M, EDGES):
  print("Yes")
else:
  print("No")