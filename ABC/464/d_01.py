T = int(input())

for _ in range(T):
  N = int(input())
  S = str(input())
  X_LIST = list(map(int, input().split()))
  Y_LIST = list(map(int, input().split()))

  def COST(i, WEATHER):
    if S[i] == "S":
      ORIGINAL = 1
    else:
      ORIGINAL = 0
    
    if ORIGINAL == WEATHER:
      return 0
    else:
      return X_LIST[i]
  
  DP_R = -(COST(0, 0))
  DP_S = -(COST(0, 1))

  for i in range(N-1):
    NEXT_R = max(DP_R, DP_S) - COST(i+1, 0)
    NEXT_S = max(DP_R + Y_LIST[i], DP_S) - COST(i+1, 1)

    DP_R = NEXT_R
    DP_S = NEXT_S
  
  print(max(DP_R, DP_S))