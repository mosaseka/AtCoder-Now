from itertools import combinations

N, M = map(int, input().split())
AB_LIST = [tuple(map(int, input().split())) for i in range(M)]

CURRENT = set()
for A, B in AB_LIST:
  CURRENT.add((min(A, B), max(A, B)))

ALL = set()
for i in range(1, N + 1):
  for j in range(i + 1, N + 1):
    ALL.add((i, j))

TARGET = N

MIN = float('inf')

for TARGET_EDGES in combinations(ALL, TARGET):
  TARGET_SET = set(TARGET_EDGES)
  
  DEGREE = [0] * (N + 1)
  for A, B in TARGET_SET:
    DEGREE[A] += 1
    DEGREE[B] += 1

  if all(DEGREE[i] == 2 for i in range(1, N + 1)):
    DELETE = len(CURRENT - TARGET_SET)
    PLUS = len(TARGET_SET - CURRENT)
    TOTAL = DELETE + PLUS
    MIN = min(MIN, TOTAL)

print(MIN)