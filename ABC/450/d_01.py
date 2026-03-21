N, K = map(int, input().split())
A_LIST = list(map(int, input().split()))

CHECK = []
for i in range(N):
  CHECK.append(A_LIST[i] % K)

CHECK.sort()

ANSWER = CHECK[0] + K - CHECK[-1]

for i in range(N - 1):
  ANSWER = max(ANSWER, CHECK[i+1] - CHECK[i])

print(K - ANSWER)