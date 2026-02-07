N, K = map(int, input().split())
ANSWER = 0

for i in range(1, N+1):
  CHECK = str(i)
  COUNT = 0
  for j in range(len(CHECK)):
    COUNT += int(CHECK[j])
  if COUNT == K:
    ANSWER += 1

print(ANSWER)