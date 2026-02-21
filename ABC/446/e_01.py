from collections import deque, defaultdict

M, A, B = map(int, input().split())

REVERSE = defaultdict(list)

for a in range(M):
  for b in range(M):
    if a == 0 or b == 0:
      continue
    NEXT = (b, (A*b + B*a) % M)
    REVERSE[NEXT].append((a, b))

NG = set()
DEQUE = deque()

for a in range(1, M):
  for b in range(1, M):
    if (A*b + B*a) % M == 0:
      NG.add((a, b))
      DEQUE.append((a, b))

while DEQUE:
  CHECK = DEQUE.popleft()
  for now in REVERSE.get(CHECK, []):
    if now not in NG:
      NG.add(now)
      DEQUE.append(now)

ANSWER = 0
for x in range(1, M):
  for y in range(1, M):
    if (x, y) not in NG:
      ANSWER += 1

print(ANSWER)