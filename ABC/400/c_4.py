import math

N = int(input())
COUNT = 0
SET = set()

A = 1
while (1 << A) <= N:
  POWER = 1 << A  # 2^A
  MAX_B = int(math.isqrt(N // POWER))
  for B in range(1, MAX_B + 1):
    X = POWER * B * B
    if X <= N and X not in SET:
      SET.add(X)
      COUNT += 1
  A += 1

print(COUNT)
