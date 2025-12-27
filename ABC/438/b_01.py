N, M = map(int, input().split())
S = str(input())
T = str(input())
ANSWER = float("inf")

for i in range(N - M + 1):
  CHECK = 0
  for j in range(M):
    CHECK += (int(S[i+j]) - int(T[j])) % 10
  ANSWER = min(ANSWER, CHECK)

print(ANSWER)