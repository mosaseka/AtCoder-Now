N = int(input())
XY_LIST = [tuple(map(int, input().split())) for _ in range(N)]

LIST = [0] * (N+1)

for x, y in XY_LIST:
  LIST[x] = y

ANSWER = 0
MIN = (N+1)

for x in range(1, N+1):
  y = LIST[x]
  if y < MIN:
    ANSWER += 1
    MIN = y

print(ANSWER)