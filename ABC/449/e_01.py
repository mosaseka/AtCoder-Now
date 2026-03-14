from collections import defaultdict, Counter
from bisect import bisect_left

class Fenwick:
  def __init__(self, n: int):
    self.n = n
    self.bit = [0] * (n + 1)

  def add(self, i: int, x: int) -> None:
    while i <= self.n:
      self.bit[i] += x
      i += i & -i

  def sum(self, i: int) -> int:
    S = 0
    while i > 0:
      S += self.bit[i]
      i -= i & -i
    return S

  def kth(self, k: int) -> int:
    IDX = 0
    BIT_MASK = 1 << (self.n.bit_length())
    while BIT_MASK:
      NXT = IDX + BIT_MASK
      if NXT <= self.n and self.bit[NXT] < k:
        k -= self.bit[NXT]
        IDX = NXT
      BIT_MASK >>= 1
    return IDX + 1


N, M = map(int, input().split())
A_LIST = list(map(int, input().split()))
Q = int(input())
X_LIST = [int(input()) for i in range(Q)]

CNT = [0] * (M + 1)
for i in range(N):
  CNT[A_LIST[i]] += 1

GROUPS = defaultdict(list)
for i in range(1, M + 1):
  GROUPS[CNT[i]].append(i)

LEVELS = sorted(GROUPS.keys())
R = len(LEVELS)

CNT_LEVEL = [0] * R
for i in range(R):
  CNT_LEVEL[i] = len(GROUPS[LEVELS[i]])

ACTIVE_SIZE = [0] * R
S = 0
for i in range(R):
  S += CNT_LEVEL[i]
  ACTIVE_SIZE[i] = S

FINITE_LEN = []
for i in range(R - 1):
  DELTA = LEVELS[i + 1] - LEVELS[i]
  FINITE_LEN.append(ACTIVE_SIZE[i] * DELTA)

PREF = []
ACC = 0
for i in range(len(FINITE_LEN)):
  ACC += FINITE_LEN[i]
  PREF.append(ACC)

if len(PREF) > 0:
  T_EQUALIZE = PREF[-1]
else:
  T_EQUALIZE = 0

ANS = [0] * Q
REQUESTS = []

for i in range(Q):
  X = X_LIST[i]
  if X <= N:
    ANS[i] = A_LIST[X - 1]
  else:
    Y = X - N
    if Y <= T_EQUALIZE and R > 1:
      P = bisect_left(PREF, Y)
      if P > 0:
        PREV = PREF[P - 1]
      else:
        PREV = 0
      SIZE = ACTIVE_SIZE[P]
      K = (Y - PREV - 1) % SIZE + 1
      REQUESTS.append((P, K, i))
    else:
      T = Y - T_EQUALIZE
      ANS[i] = (T - 1) % M + 1

REQUESTS.sort()
FW = Fenwick(M)
CUR_PHASE = -1

for i in range(len(REQUESTS)):
  P, K, QI = REQUESTS[i]
  while CUR_PHASE < P:
    CUR_PHASE += 1
    LV = LEVELS[CUR_PHASE]
    for j in range(len(GROUPS[LV])):
      V = GROUPS[LV][j]
      FW.add(V, 1)
  ANS[QI] = FW.kth(K)

for i in range(Q):
  print(ANS[i])