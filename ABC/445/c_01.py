N = int(input())
A_LIST = list(map(int, input().split()))

FINAL = [0] * (N+1)

for i in range(1, N+1):
  PATH = []
  VISITED = {}
  NOW = i
  
  while NOW not in VISITED:
    VISITED[NOW] = len(PATH)
    PATH.append(NOW)
    NOW = A_LIST[NOW-1]

  CYCLE_START = VISITED[NOW]
  CYCLE_LEN = len(PATH) - CYCLE_START

  REMAIN = (10**100 - CYCLE_START) % CYCLE_LEN
  FINAL[i] = PATH[CYCLE_START + REMAIN]

print(*FINAL[1:])