from math import sqrt

N = int(input())
COUNT = [0] * (N + 1)
ANSWER = []

MAX = int(sqrt(N)) + 1

for x in range(1, MAX):
  if x**2 >= N:
    break
  for y in range(x + 1, MAX):
    n = x**2 + y**2
    if n > N:
      break
    COUNT[n] += 1

for i in range(1, N + 1):
  if COUNT[i] == 1:
      ANSWER.append(i)

print(len(ANSWER))
print(*ANSWER)