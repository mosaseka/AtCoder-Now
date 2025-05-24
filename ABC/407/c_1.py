from collections import deque

S = deque(map(int, input()))
ANSWER = 0
MINUS = 0

while S:
  LAST = (S[-1] - MINUS) % 10
  if LAST == 0:
    S.pop()
    ANSWER += 1
  else:
    MINUS += 1
    ANSWER += 1

print(ANSWER)