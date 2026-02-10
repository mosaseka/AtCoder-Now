from collections import defaultdict

G = defaultdict(list)

N, M = map(int, input().split())

for _ in range(M):
  A, B = map(int, input().split())
  G[A].append(B)
  G[B].append(A)

for i in range(1, N + 1):
  if len(G[i]) > 2:
    print("No")
    exit()

visited = set()
valid = True

for i in range(1, N + 1):
  if i in visited:
    continue
  stack = [(i, 0)]
  visited.add(i)
  start = i
  while stack:
    pos, prev = stack.pop()
    for next_node in G[pos]:
      if next_node == prev:
        continue
      if next_node in visited:
        if next_node == start:
          valid = False
          break
      else:
        visited.add(next_node)
        stack.append((next_node, pos))
    if not valid:
      break
  if not valid:
    break

print("Yes" if valid else "No")