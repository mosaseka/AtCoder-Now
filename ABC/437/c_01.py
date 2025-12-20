T = int(input())

for i in range(T):
  CHECK = []
  N = int(input())
  for j in range(N):
    W, P = map(int, input().split())
    CHECK.append([W, P])
  CHECK.sort(key=lambda x: x[0]+x[1])
  TOTAL = sum(p for w, p in CHECK)
  RIDE = 0
  PULL = TOTAL
  ANSWER = 0
  for w, p in CHECK:
    RIDE_NEW = RIDE + w
    PULL_NEW = PULL - p
    if PULL_NEW >= RIDE_NEW:
      RIDE = RIDE_NEW
      PULL = PULL_NEW
      ANSWER += 1
  print(ANSWER)