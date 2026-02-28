class UnionFind():
  PAR = []
  SIZ = []

  def __init__(self, x):
    self.PAR = [-1 for n in range(x)]
    self.SIZ = [1 for n in range(x)]

  def root(self, x):
    if self.PAR[x] == -1:
      return x
    else:
      self.PAR[x] = self.root(self.PAR[x])
      return self.PAR[x]

  def issame(self, x, y):
    if self.root(x) == self.root(y):
      return True
    else:
      return False

  def unite(self, x, y):
    x = self.root(x)
    y = self.root(y)
    if x == y:
      return False
    if self.SIZ[x] < self.SIZ[y]:
      x, y = y, x
    self.PAR[y] = x
    self.SIZ[x] += self.SIZ[y]
    return True

  def size(self, x):
    return self.SIZ[self.root(x)]

N, M = map(int, input().split())
UV_LIST = [tuple(map(int, input().split())) for _ in range(M)]

UF = UnionFind(N)
COUNT = N
DELETED = []

for i in range(M-1, -1, -1):
  u, v = UV_LIST[i]
  if UF.issame(u-1, v-1):
    continue
  if COUNT <= 2:
    DELETED.append(i+1)
  else:
    UF.unite(u-1, v-1)
    COUNT -= 1

ANS = 0
for eid in DELETED:
  ANS = (ANS + pow(2, eid, 998244353)) % 998244353
print(ANS)