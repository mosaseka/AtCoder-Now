N = int(input())
SET = set()

for i in range(N):
  A, B = map(int, input().split())
  if (A, B) == (0, 0):
    SET.add(i+1)
  elif A in SET:
    SET.add(i+1)
  elif B in SET:
    SET.add(i+1)

print(len(SET))