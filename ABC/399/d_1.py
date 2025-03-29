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

    POS = sorted(POS_A + POS_B)
    if (abs(POS[0] - POS[1]) == 1 and abs(POS[2] - POS[3]) == 1):
      RESULT += 1

  print(RESULT)

T = int(input())
for _ in range(T):
  SOLVE()