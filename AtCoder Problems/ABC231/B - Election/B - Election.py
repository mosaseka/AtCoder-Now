N = int(input())

COUNT = dict()

for _ in range(N):
  S = str(input())
  COUNT[S] = COUNT.get(S, 0) + 1

ANSWER = ""
MAX = 0

for key, value in COUNT.items():
  if value > MAX:
    MAX = value
    ANSWER = key

print(ANSWER)