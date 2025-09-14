N = int(input())
L_LIST = list(map(int, input().split()))
SET = set()

SET.add(0)
SET.add(N)

for i in range(N):
  if L_LIST[i] == 0:
    SET.add(i + 1)
  else:
    break

for i in range(N - 1, -1, -1):
  if L_LIST[i] == 0:
    SET.add(i)
  else:
    break

print((N + 1) - len(SET))