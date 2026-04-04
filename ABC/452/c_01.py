N = int(input())
AB_LIST = [tuple(map(int, input().split())) for i in range(N)]
M = int(input())
S_LIST = [input() for i in range(M)]

POOL = [[set() for j in range(10)] for i in range(11)]

for TEXT in S_LIST:
  for k in range(len(TEXT)):
    POOL[len(TEXT)][k].add(TEXT[k])

NEED = [set() for i in range(N)]
for i in range(N):
  NEED[i] = POOL[AB_LIST[i][0]][AB_LIST[i][1] - 1]

ANSWER = []
for TEXT in S_LIST:
  if len(TEXT) != N:
    ANSWER.append("No")
    continue
  OK = True
  for i in range(N):
    if TEXT[i] not in NEED[i]:
      OK = False
      break
  if OK:
    ANSWER.append("Yes")
  else:
    ANSWER.append("No")

print("\n".join(ANSWER))