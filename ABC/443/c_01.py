N, T = map(int, input().split())
A = list(map(int, input().split()))

NOW = 0
ANSWER = 0

for a in A:
  if a < NOW:
    continue
  ANSWER += a - NOW
  NOW = a + 100

if NOW < T:
  ANSWER += T - NOW

print(ANSWER)