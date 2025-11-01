T = int(input())

for i in range(T):
  A = str(input())
  B = str(input())
  CHECK = len(A)
  A = int(A, 2)
  B = int(B, 2)
  if A == B:
    print(0)
    continue
  FLAG = False
  for j in range(1, CHECK):
    TOP = (A >> (CHECK - 1)) & 1
    A = ((A << 1) | TOP) & ((1 << CHECK) - 1)
    if A == B:
      print(j)
      FLAG = True
      break
  if not FLAG:
    print(-1)