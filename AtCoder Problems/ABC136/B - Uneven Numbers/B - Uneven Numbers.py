N = int(input())

ANSWER = 0

for i in range(1, N + 1):
  if 1 <= i <= 9:
    ANSWER += 1
  elif 100 <= i <= 999:
    ANSWER += 1
  elif 10000 <= i <= 99999:
    ANSWER += 1

print(ANSWER)