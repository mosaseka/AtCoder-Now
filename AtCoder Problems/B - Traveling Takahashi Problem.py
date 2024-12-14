import math

N = int(input())
PAST = [0, 0]
ANSWER = 0

for i in range(N):
  NOW = list(map(int, input().split()))
  ANSWER += math.sqrt((PAST[0] - NOW[0])**2 + (PAST[1] - NOW[1])**2)
  PAST = NOW

print(ANSWER)