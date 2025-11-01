T = int(input())

for i in range(T):
  A = str(input())
  B = str(input())
  CHECK = len(A)
  DOUBLE_A = A + A
  POSITION = DOUBLE_A.find(B)
  if POSITION >= 0:
    print(POSITION)
  else:
    print(-1)