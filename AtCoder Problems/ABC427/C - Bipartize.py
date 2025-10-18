N, M = map(int, input().split())
UV_LIST = [tuple(map(int, input().split())) for i in range(M)]
ANSWER = M

for i in range(2**N):
  COUNT = 0
  for U, V in UV_LIST:
    if (1 & (i >> U)) == (1 & (i >> V)):
      COUNT += 1
  ANSWER = min(ANSWER, COUNT)

print(ANSWER)