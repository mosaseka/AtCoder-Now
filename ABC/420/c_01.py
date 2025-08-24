N, Q = map(int, input().split())
A_LIST = list(map(int, input().split()))
B_LIST = list(map(int, input().split()))
QUERY = []
X = ""
X = 0
V = 0
SUM = 0

for i in range(N):
  SUM += min(A_LIST[i], B_LIST[i])

for i in range(Q):
  QUERY = list(map(str, input().split()))
  C = QUERY[0]
  X = int(QUERY[1])
  V = int(QUERY[2])
  if C == "A":
    if V < B_LIST[X - 1]:
      SUM += V - A_LIST[X - 1]
    A_LIST[X - 1] = V
  elif C == "B":
    if V < A_LIST[X - 1]:
      SUM += V - B_LIST[X - 1]
    B_LIST[X - 1] = V
  print(SUM)