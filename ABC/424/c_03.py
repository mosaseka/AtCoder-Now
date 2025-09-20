from collections import deque, defaultdict

N = int(input())
DEPEND = defaultdict(list)
LEARNED = set()
QUEUE = deque()
SKILLS = []

for i in range(N):
  A, B = map(int, input().split())
  SKILLS.append((A, B))
  if (A, B) == (0, 0):
    LEARNED.add(i + 1)
    QUEUE.append(i + 1)
  else:
    if A != 0:
      DEPEND[A].append(i + 1)
    if B != 0:
      DEPEND[B].append(i + 1)

#BFS
while QUEUE:
  NOW = QUEUE.popleft()
  for NEXT in DEPEND[NOW]:
    if NEXT not in LEARNED:
      INDEX = NEXT - 1
      A, B = SKILLS[INDEX]
      POSSIBLE = False
      if A == 0:
        POSSIBLE = B in LEARNED
      elif B == 0:
        POSSIBLE = A in LEARNED
      else:
        POSSIBLE = A in LEARNED or B in LEARNED
      if POSSIBLE:
        LEARNED.add(NEXT)
        QUEUE.append(NEXT)

print(len(LEARNED))