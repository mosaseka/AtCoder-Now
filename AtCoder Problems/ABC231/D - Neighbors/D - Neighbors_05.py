def FIND(X, PARENT):
  while PARENT[X] != X:
    PARENT[X] = PARENT[PARENT[X]]
    X = PARENT[X]
  return X

def UNION(A, B, PARENT, SIZE):
  RA = FIND(A, PARENT)
  RB = FIND(B, PARENT)
  if RA == RB:
    return False
  if SIZE[RA] < SIZE[RB]:
    RA, RB = RB, RA
  PARENT[RB] = RA
  SIZE[RA] += SIZE[RB]
  return True

N, M = map(int, input().split())
PARENT = list(range(N))
SIZE = [1] * N
DEG = [0] * N

for i in range(M):
  A, B = map(int, input().split())
  A -= 1
  B -= 1
  if not UNION(A, B, PARENT, SIZE):
    print("No")
    exit()
  DEG[A] += 1
  DEG[B] += 1

for i in range(N):
  if DEG[i] > 2:
    print("No")
    exit()

print("Yes")