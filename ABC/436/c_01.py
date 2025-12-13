N, M = map(int, input().split())
CHECK = set()
ANSWER = 0

for i in range(M):
  R, C = map(int, input().split())
  CELL = [(R, C), (R + 1, C), (R, C + 1), (R + 1, C + 1)]
  FLAG = True
  for cell in CELL:
    if cell in CHECK:
      FLAG = False
      break
  if FLAG:
    ANSWER += 1
    for j in CELL:
      CHECK.add(j)

print(ANSWER)