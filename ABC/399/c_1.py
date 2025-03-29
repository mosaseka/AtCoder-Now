N, M = map(int, input().split())
EDGE = []
for _ in range(M):
  A, B = map(int, input().split())
  A -= 1
  B -= 1
  EDGE.append((A, B))

class UNIONFIND:
  def __init__(self, N):
    self.PARENT = list(range(N))
    self.RANK = [0] * N

  def FIND(self, X):
    if self.PARENT[X] != X:
      self.PARENT[X] = self.FIND(self.PARENT[X])
    return self.PARENT[X]

  def UNION(self, X, Y):
    ROOT_X = self.FIND(X)
    ROOT_Y = self.FIND(Y)
    if ROOT_X == ROOT_Y:
      return False
    if self.RANK[ROOT_X] < self.RANK[ROOT_Y]:
      self.PARENT[ROOT_X] = ROOT_Y
    elif self.RANK[ROOT_X] > self.RANK[ROOT_Y]:
      self.PARENT[ROOT_Y] = ROOT_X
    else:
      self.PARENT[ROOT_Y] = ROOT_X
      self.RANK[ROOT_X] += 1
    return True

UF = UNIONFIND(N)
CYCLE_COUNT = 0

for A, B in EDGE:
  if not UF.UNION(A, B):
    CYCLE_COUNT += 1

print(CYCLE_COUNT)