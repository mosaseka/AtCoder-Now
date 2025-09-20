from collections import deque

N = int(input())
SKILLS = []
LEARNED = set()
QUEUE = deque()

for i in range(N):
  A, B = map(int, input().split())
  SKILLS.append((A, B))
  if (A, B) == (0, 0):
    LEARNED.add(i + 1)
    QUEUE.append(i + 1)

#BFS
while QUEUE:
  CURRENT_SKILL = QUEUE.popleft()
  for i in range(N):
    SKILL_NUM = i + 1
    A, B = SKILLS[i]
    if SKILL_NUM not in LEARNED:
      POSSIBLE = False
      if A == 0 and B == 0:
        continue
      elif A == 0:
        POSSIBLE = B in LEARNED
      elif B == 0:
        POSSIBLE = A in LEARNED
      else:
        POSSIBLE = A in LEARNED or B in LEARNED
      if POSSIBLE:
        LEARNED.add(SKILL_NUM)
        QUEUE.append(SKILL_NUM)

print(len(LEARNED))