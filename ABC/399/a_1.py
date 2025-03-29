N = int(input())
S = str(input())
T = str(input())
COUNT = 0

for i in range(N):
  if S[i] != T[i]:
    COUNT += 1

print(COUNT)