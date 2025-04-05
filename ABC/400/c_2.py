import math

N = int(input())
SET = set()

A = 1
while (1 << A) <= N:
  POWER = 1 << A
  LIMIT = N // POWER
  MAX_B = int(math.isqrt(LIMIT))
  for B in range(1, MAX_B + 1):
    VAL = POWER * (B * B)
    SET.add(VAL)
  A += 1

print(len(SET))