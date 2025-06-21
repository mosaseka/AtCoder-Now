N, Q = map(int, input().split())
PC = [[] for i in range(N + 1)]
SERVER = []

for i in range(Q):
  QUERY = list(map(str, input().split()))
  if QUERY[0] == "1":
    P = int(QUERY[1])
    PC[P] = SERVER[:]
  elif QUERY[0] == "2":
    P = int(QUERY[1])
    S = QUERY[2]
    PC[P].append(S)
  elif QUERY[0] == "3":
    P = int(QUERY[1])
    SERVER = PC[P][:]

print("".join(SERVER))