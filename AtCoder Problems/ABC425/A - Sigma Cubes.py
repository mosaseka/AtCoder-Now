N = int(input())
ANSWER = 0

for i in range(1, N+1):
  ANSWER += (-1)**i * i**3

print(ANSWER)