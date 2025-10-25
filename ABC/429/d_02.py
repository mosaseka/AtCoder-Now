from collections import Counter

N, M, C = map(int, input().split())
A = list(map(int, input().split()))
COUNTER = Counter()
POSITION = []
COUNT = []
K = 0
POSITION_2 = []
COUNT_2 = []
PREF = []
TOTAL = 0
ANSWER = 0
MET = 0
GAP = 0
CHECK = 0

COUNTER = Counter(A)
if not COUNTER:
  print(0)
  exit()

POSITION = sorted(COUNTER.keys())
COUNT = [COUNTER[i] for i in POSITION]
K = len(POSITION)

POSITION_2 = POSITION + [i + M for i in POSITION]
COUNT_2 = COUNT + COUNT

PREF = [0]
for i in COUNT_2:
  PREF.append(PREF[-1] + i)

TOTAL = PREF[K]

for i in range(K):
  CHECK = max(CHECK, i)
  while CHECK < i + K and (PREF[CHECK + 1] - PREF[i + 1] < C):
    CHECK += 1
  MET = PREF[CHECK + 1] - PREF[i + 1]
  if i < K - 1:
    GAP = POSITION[i + 1] - POSITION[i]
  else:
    GAP = M - POSITION[i] + POSITION[0]
  ANSWER += MET * GAP

print(ANSWER)