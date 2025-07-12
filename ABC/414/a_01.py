N, L, R = map(int, input().split())
COUNT = 0

for i in range(N):
  X, Y = map(int, input().split())
  if X <= L and R <= Y:
    COUNT += 1

print(COUNT)