N, Q = map(int, input().split())
PC = [""] * (N + 1)
SERVER = ""

for i in range(Q):
  QUERY = list(map(str, input().split()))
  if QUERY[0] == "1":
    PC[int(QUERY[1])] = SERVER
  elif QUERY[0] == "2":
    PC[int(QUERY[1])] += QUERY[2]
  elif QUERY[0] == "3":
    SERVER = PC[int(QUERY[1])]

print(SERVER)