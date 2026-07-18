N, M = map(int, input().split())
A_LIST = list(map(int, input().split()))
B_LIST = list(map(int, input().split()))

NOW = 0
PLUS = 0
MINUS = 0
SIGN = 1
OFFSET = 0
DICT = dict()

for i in range(N):
  NOW += OFFSET

  if SIGN == 1:
    PLUS += 1
    CHECK = (-OFFSET) % M
    if CHECK != 0:
      DICT[CHECK] = DICT.get(CHECK, 0) - M
  
  else:
    MINUS += 1
    CHECK = OFFSET + 1
    if CHECK < M:
      DICT[CHECK] = DICT.get(CHECK, 0) + M
  
  if i < N-1:
    DIFF = (B_LIST[i] - A_LIST[i] - A_LIST[i+1]) % M
    OFFSET = (DIFF - OFFSET) % M
    SIGN *= -1

ANSWER = NOW
LAST = 0

for key in sorted(DICT):
  NOW += (PLUS - MINUS) * (key - LAST)
  NOW += DICT[key]
  ANSWER = min(ANSWER, NOW)
  LAST = key

print(ANSWER)