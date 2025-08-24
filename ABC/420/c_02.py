N, Q = map(int, input().split())
A_LIST = list(map(int, input().split()))
B_LIST = list(map(int, input().split()))

SUM = sum(min(A_LIST[i], B_LIST[i]) for i in range(N))

for _ in range(Q):
  QUERY = input().split()
  C = QUERY[0]
  X = int(QUERY[1]) - 1
  V = int(QUERY[2])
  
  SUM -= min(A_LIST[X], B_LIST[X])
  
  if C == "A":
    A_LIST[X] = V
  else:
    B_LIST[X] = V
  
  SUM += min(A_LIST[X], B_LIST[X])
  
  print(SUM)