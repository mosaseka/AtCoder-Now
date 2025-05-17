N, K = map(int, input().split())
A = list(map(int, input().split()))
ANSWER = 1

for i in range(N):
  ANSWER *= A[i]
  if len(str(ANSWER)) > K:
    ANSWER = 1

print(ANSWER)