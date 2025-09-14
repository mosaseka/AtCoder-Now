N, R = map(int, input().split())
L_LIST = list(map(int, input().split()))

OPEN = []
for i, x in enumerate(L_LIST):
  if x == 0:
    OPEN.append(i)

if not OPEN:
  print(0)
  exit()

CURRENT = len(OPEN)
LEFT_OPEN = min(OPEN)
RIGHT_OPEN = max(OPEN)

LEFT_CROSS = 0
for j in range(LEFT_OPEN + 1, R):
  if L_LIST[j] == 1:
    LEFT_CROSS += 1

RIGHT_CROSS = 0
for j in range(R, RIGHT_OPEN):
  if L_LIST[j] == 1:
    RIGHT_CROSS += 1

ANS = CURRENT + 2 * (LEFT_CROSS + RIGHT_CROSS)
print(ANS)