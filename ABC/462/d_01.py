N, D = map(int, input().split())

MAX = 10**6 + 2
DIFF = [0] * (MAX+1)
ANSWER = 0
ACTIVE = 0

for _ in range(N):
  S, T = map(int, input().split())
  
  LEFT = S
  RIGHT = T - D

  if LEFT <= RIGHT:
    DIFF[LEFT] += 1
    DIFF[RIGHT+1] -= 1

for i in range(MAX):
  ACTIVE += DIFF[i]
  ANSWER += (ACTIVE-1) * ACTIVE // 2

print(ANSWER)