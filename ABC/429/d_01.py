from collections import defaultdict
from bisect import bisect_left

N, M, C = map(int, input().split())
A_LIST = list(map(int, input().split()))

COUNT = defaultdict(int)
CUM_SUM = [0]
POSITIONS = []
TOTAL_PEOPLE = 0
TOTAL = 0
INTERVAL = 0
NEXT = 0
PEOPLE = 0
STOP = 0
MET = 0
TARGET_LIST = []
NUM_POSITIONS = 0

for i in A_LIST:
  COUNT[i] += 1

POSITIONS = sorted(COUNT.keys())

if not POSITIONS:
  print(0)
  exit()

for i in POSITIONS:
  CUM_SUM.append(CUM_SUM[-1] + COUNT[i])

TOTAL_PEOPLE = CUM_SUM[-1]
NUM_POSITIONS = len(POSITIONS)

for i in range(NUM_POSITIONS):
  if i == NUM_POSITIONS - 1:
    INTERVAL = M - POSITIONS[i] + POSITIONS[0]
  else:
    INTERVAL = POSITIONS[i + 1] - POSITIONS[i]
  
  TARGET_LIST = []
  for j in range(1, NUM_POSITIONS + 1):
    NEXT = (i + j) % NUM_POSITIONS
    if NEXT > i:
      PEOPLE = CUM_SUM[NEXT + 1] - CUM_SUM[i + 1]
    else:
      PEOPLE = TOTAL_PEOPLE - CUM_SUM[i + 1] + CUM_SUM[NEXT + 1]
    TARGET_LIST.append(PEOPLE)
  
  IDX = bisect_left(TARGET_LIST, C)
  
  if IDX < NUM_POSITIONS:
    STOP = (i + IDX + 1) % NUM_POSITIONS
  else:
    STOP = i
  
  if STOP > i:
    MET = CUM_SUM[STOP + 1] - CUM_SUM[i + 1]
  else:
    MET = TOTAL_PEOPLE - CUM_SUM[i + 1] + CUM_SUM[STOP + 1]
  
  TOTAL += MET * INTERVAL

print(TOTAL)