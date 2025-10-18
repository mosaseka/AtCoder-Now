N, Q = map(int, input().split())
A_LIST = list(map(int, input().split()))
MOVE_COUNT = 0

for i in range(Q):
  QUERY = list(map(int, input().split()))
  if QUERY[0] == 1:
    C = QUERY[1]
    MOVE_COUNT = (MOVE_COUNT + C) % N
  else:
    L, R = QUERY[1], QUERY[2]
    TOTAL = 0
    for j in range(L, R + 1):
      NOW = (j - 1 + MOVE_COUNT) % N
      TOTAL += A_LIST[NOW]
    print(TOTAL)