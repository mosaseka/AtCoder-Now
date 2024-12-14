N,R = map(int, input().split())
D = 0
A = 0

for i in range(N):
  D,A = map(int, input().split())
  if D == 1:
    if 1600 <= R <= 2799:
      R += A
  else:
    if 1200 <= R <= 2399:
      R += A

print(R)