import math

N = int(input())
SET = set()

B_MAX = int(1e5)

for B in range(1, B_MAX + 1):
  BASE = B * B
  LIMIT = N // BASE
  if LIMIT == 0:
    continue
  MAX_POW = LIMIT.bit_length() - 1
  for A in range(1, MAX_POW + 1):
    VAL = BASE << A
    if VAL <= N:
      SET.add(VAL)
    else:
      break

print(len(SET))