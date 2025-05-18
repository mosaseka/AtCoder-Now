N, M, Q = map(int, input().split())
VIEW = [set() for i in range(N)]
ALL = [False] * N

for i in range(Q):
  QUERY = list(map(int, input().split()))
  if QUERY[0] == 1:
    VIEW[QUERY[1]-1].add(QUERY[2]-1)
  elif QUERY[0] == 2:
    ALL[QUERY[1]-1] = True
  elif QUERY[0] == 3:
    if QUERY[2] - 1 in VIEW[QUERY[1]-1] or ALL[QUERY[1]-1]:
      print("Yes")
    else:
      print("No")