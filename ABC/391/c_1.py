from collections import defaultdict

N, Q = map(int, input().split())
PIGION = list(range(N)) 
NEST = [1] * N
MULTI = 0

for i in range(Q):
  QUERY = list(map(int, input().split()))
  if QUERY[0] == 1:
    P = QUERY[1] - 1
    H = QUERY[2] - 1
    CULLENT = PIGION[P]
        
    NEST[CULLENT] -= 1
    if NEST[CULLENT] == 1:
      MULTI -= 1
        
    PIGION[P] = H
    NEST[H] += 1
    if NEST[H] == 2:
      MULTI += 1
  elif QUERY[0] == 2:
    print(MULTI)