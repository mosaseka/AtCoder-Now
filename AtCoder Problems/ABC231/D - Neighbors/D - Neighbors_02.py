from collections import defaultdict

visited = set()
G = defaultdict(list)

def dfs(pos, start, prev):
  visited.add(pos)
  for next_node in G[pos]:
    if next_node != prev and next_node in visited and next_node == start:
      return False
    if next_node not in visited:
      if not dfs(next_node, start, pos):
        return False
  return True

N, M = map(int, input().split())

for _ in range(M):
  A, B = map(int, input().split())
  G[A].append(B)
  G[B].append(A)


valid = True
for i in range(1, N + 1):
  if len(G[i]) > 2:
    valid = False
    break

if valid:
  for i in range(1, N + 1):
    if i not in visited:
      if not dfs(i, i, 0):
        valid = False
        break

print("Yes" if valid else "No")