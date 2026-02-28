N = int(input())

ANSWER = N + 1 - 2

for i in range(1, int(N**0.5) + 1):
  if N % i == 0:
    ANSWER = min(ANSWER, N//i + i - 2)

print(ANSWER)