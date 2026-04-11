T, X = map(int, input().split())
A_LIST = list(map(int, input().split()))

ANSWER = []

for i in range(T+1):
  if i == 0:
    ANSWER.append([i, A_LIST[i]])
  else:
    if abs(A_LIST[i] - ANSWER[-1][1]) >= X:
      ANSWER.append([i, A_LIST[i]])

for ans in ANSWER:
  print(*ans)