class Fenwick_Tree:
  def __init__(self, n):
    self._n = n
    self.data = [0] * n

  def add(self, p, x):
    assert 0 <= p < self._n
    p += 1
    while p <= self._n:
      self.data[p - 1] += x
      p += p & (-p)
  
  def _sum(self, r):
    s = 0
    while r > 0:
      s += self.data[r - 1]
      r -= r & (-r)
    return s
  
  def sum(self, l, r):
    assert 0 <= l <= r <= self._n
    return self._sum(r) - self._sum(l)

N, Q = map(int, input().split())

RAW = [0] * N

BIT = Fenwick_Tree(N)
BIT.add(0, N)

OFFSET = 0
MIN = 0

for _ in range(Q):
  QUERY = list(map(int, input().split()))
  match QUERY[0]:
    case 1:
      X = QUERY[1] - 1
      OLD = RAW[X]
      NEW = OLD + 1
      RAW[X] = NEW

      BIT.add(OLD, -1)
      BIT.add(NEW, 1)

      while MIN < Q and BIT.sum(0, MIN+1) - BIT.sum(0, MIN) == 0:
        MIN += 1
      
      if MIN >= OFFSET+1:
        OFFSET += 1
    case 2:
      Y = QUERY[1]
      CHECK = OFFSET + Y

      if CHECK > Q:
        print(0)
      else:
        LESS = BIT.sum(0, CHECK)
        print(N - LESS)