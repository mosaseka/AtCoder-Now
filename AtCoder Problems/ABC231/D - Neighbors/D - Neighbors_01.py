class State:
  flag = True
  visited = None
  G = None

def dfs(pos, start, prev):
  State.visited[pos] = True
  for next in State.G[pos]:
    if not State.flag:
      return
    if next != prev and State.visited[next] and next == start:
      State.flag = False
      return
    if not State.visited[next]:
      dfs(next, start, pos)

N, M = map(int, input().split())

State.G = [[] for _ in range(N+1)]

for _ in range(M):
  A, B = map(int, input().split())
  State.G[A].append(B)
  State.G[B].append(A)

for i in range(1, N+1):
  if 2 < len(State.G[i]):
    print("No")
    exit()

State.visited = [False] * (N+1)
State.flag = True

for i in range(1, N+1):
  if State.visited[i]:
    continue
  dfs(i, i, 0)

print("Yes" if State.flag else "No")