T = int(input())

for i in range(T):
  N, W = map(int, input().split())
  C_LIST = list(map(int, input().split()))
  SUM_LIST = [0] * (2 * W)

  for i, ci in enumerate(C_LIST, start=1):
    SUM_LIST[i % (2 * W)] += ci

  DOUBLE_SUM_LIST = SUM_LIST * 2
  CHECK = sum(DOUBLE_SUM_LIST[:W])
  ANSWER = CHECK

  for j in range(1, 2 * W):
    CHECK += DOUBLE_SUM_LIST[j + W - 1] - DOUBLE_SUM_LIST[j - 1]
    ANSWER = min(ANSWER, CHECK)
    
  print(ANSWER)