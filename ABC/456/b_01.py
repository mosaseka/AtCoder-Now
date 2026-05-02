from itertools import permutations

A = [list(map(int, input().split())) for _ in range(3)]

ANSWER = 0

for perm in permutations([4, 5, 6]):
  CHECK = 1
  for i in range(3):
    CHECK *= A[i].count(perm[i])
  ANSWER += CHECK

print(ANSWER / (6**3))