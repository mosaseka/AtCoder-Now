N = int(input())
A_LIST = list(map(int, input().split()))

ANSWER = [0] * (N+1)
DONE = [False] * (N+1)

for start in range(1, N+1):
  if DONE[start]:
    continue

  PATH = []
  INDEX = {}
  NOW = start

  while NOW  not in INDEX and not DONE[NOW]:
    INDEX[NOW] = len(PATH)
    PATH.append(NOW)
    NOW = A_LIST[NOW-1]
  
  if DONE[NOW]:
    for i in range(len(PATH)-1, -1, -1):
      ANSWER[PATH[i]] = ANSWER[NOW]
      DONE[PATH[i]] = True
      NOW = PATH[i]
  else:
    CYCLE_START = INDEX[NOW]
    CYCLE_LEN = len(PATH) - CYCLE_START
    STEP = pow(10, 100, CYCLE_LEN)

    for i in range(CYCLE_START, len(PATH)):
      FINAL = CYCLE_START + (i - CYCLE_START + STEP) % CYCLE_LEN
      ANSWER[PATH[i]] = PATH[FINAL]
      DONE[PATH[i]] = True
    
    for i in range(CYCLE_START-1, -1, -1):
      ANSWER[PATH[i]] = ANSWER[PATH[i+1]]
      DONE[PATH[i]] = True

print(*ANSWER[1:])