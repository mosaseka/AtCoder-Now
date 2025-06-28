T = int(input())

for i in range(T):
  N = int(input())
  S_LIST = list(map(int, input().split()))
  FIRST = S_LIST[0]
  FINAL = S_LIST[-1]
  
  if FINAL <= 2 * FIRST:
    print(2)
    continue

  USED = [False] * N
  USED[0] = True
  CURRENT_POWER = FIRST
  COUNT = 1
  
  while True:
    if 2 * CURRENT_POWER >= FINAL:
      COUNT += 1
      print(COUNT)
      break
    
    BEST_SIZE = 0
    BEST_IDX = -1
    
    for j in range(1, N-1):
      if not USED[j] and S_LIST[j] <= 2 * CURRENT_POWER:
        if S_LIST[j] > BEST_SIZE:
          BEST_SIZE = S_LIST[j]
          BEST_IDX = j
    
    if BEST_IDX == -1:
      print(-1)
      break
    
    USED[BEST_IDX] = True
    CURRENT_POWER = BEST_SIZE
    COUNT += 1