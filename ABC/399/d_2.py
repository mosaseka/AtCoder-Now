from itertools import combinations

def SOLVE():
  N = int(input())
  A = list(map(int, input().split()))

  POSITIONS = {I: [] for I in range(1, N + 1)}
  for IDX, VALUE in enumerate(A):
    POSITIONS[VALUE].append(IDX)
  
  RESULT = 0
  
  for A, B in combinations(range(1, N + 1), 2):
    POS_A = POSITIONS[A]
    POS_B = POSITIONS[B]

    if abs(POS_A[0] - POS_A[1]) == 1:
      continue

    if abs(POS_B[0] - POS_B[1]) == 1:
      continue

    INDICES = sorted(POS_A + POS_B)
    if (INDICES[1] - INDICES[0] == 1 and INDICES[3] - INDICES[2] == 1):
      RESULT += 1
  
  print(RESULT)

T = int(input())
for _ in range(T):
  SOLVE()