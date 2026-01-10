T = int(input())

for i in range(T):
  N, W = map(int, input().split())
  C_LIST = list(map(int, input().split()))
  ANSWER = float("inf")
  SUM_LIST = [0] * (2 * W)

  for i in range(1, N + 1):
    SUM_LIST[i % (2 * W)] += C_LIST[i - 1]
  
  for x in range(1, 2*W + 1):
    CHECK = 0
    for r in range(2 * W):
      if (r + x) % (2 * W) < W:
        CHECK += SUM_LIST[r]
    ANSWER = min(ANSWER, CHECK)
    
  print(ANSWER)