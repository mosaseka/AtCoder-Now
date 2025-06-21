N, Q = map(int, input().split())
PC = [[] for _ in range(N + 1)]
IS_SHARED = [False] * (N + 1)
SERVER = []

for _ in range(Q):
  QUERY = list(map(str, input().split()))
  if QUERY[0] == "1":
    P = int(QUERY[1])
    PC[P] = SERVER
    IS_SHARED[P] = True
  elif QUERY[0] == "2":
    P = int(QUERY[1])
    S = QUERY[2]
    if IS_SHARED[P]:
      PC[P] = PC[P][:]
      IS_SHARED[P] = False
    PC[P].append(S)
  elif QUERY[0] == "3":
    P = int(QUERY[1])
    SERVER = PC[P]

print("".join(SERVER))