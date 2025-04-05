N = int(input())
SET = set()

a = 1
while (2**a) <= N:
  b = 1
  while (2**a) * (b**2) <= N:
    SET.add((2**a) * (b**2))
    b += 1
  a += 1

print(len(SET))