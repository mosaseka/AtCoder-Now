def COUNT_VALID_PAIRS(TEST_CASES):
  RESULTS = []
  
  for N, A in TEST_CASES:
    POSITION = {I: [] for I in range(1, N + 1)}
    for I, VALUE in enumerate(A):
      POSITION[VALUE].append(I)
    
    ANSWERS = set()
    for I in range(len(A) - 1):
      A_VAL, B_VAL = A[I], A[I + 1]
      if POSITION[A_VAL][0] + 1 == POSITION[A_VAL][1]:
        continue
      if POSITION[B_VAL][0] + 1 == POSITION[B_VAL][1]:
        continue
      V = sorted([POSITION[A_VAL][0], POSITION[A_VAL][1], POSITION[B_VAL][0], POSITION[B_VAL][1]])
      if V[0] + 1 == V[1] and V[2] + 1 == V[3]:
        ANSWERS.add(tuple(sorted((A_VAL, B_VAL))))
    
    RESULTS.append(len(ANSWERS))
  
  return RESULTS

T = int(input())
TEST_CASES = []
for _ in range(T):
  N = int(input())
  A = list(map(int, input().split()))
  TEST_CASES.append((N, A))

for RESULT in COUNT_VALID_PAIRS(TEST_CASES):
  print(RESULT)