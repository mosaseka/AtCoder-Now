N, M, K = map(int, input().split())
LIST = [[False] * M for _ in range(N)]
ANSWER = []

for i in range(K):
  A, B = map(int, input().split())
  LIST[A-1][B-1] = True
  if all(LIST[A-1]):
    ANSWER.append(A)

print(*ANSWER)