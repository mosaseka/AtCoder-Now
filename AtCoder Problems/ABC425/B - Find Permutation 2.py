from itertools import permutations

N = int(input())
A = list(map(int, input().split()))
CHECK = [i for i in range(1, N+1)]

for P in permutations(CHECK):
  FLAG = True
  for j in range(N):
    if A[j] != -1 and P[j] != A[j]:
      FLAG = False
      break
  if FLAG:
    print("Yes")
    print(*P)
    exit()

print("No")