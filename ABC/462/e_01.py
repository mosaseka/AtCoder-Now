T = int(input())

for _ in range(T):
  A, B, X, Y = map(int, input().split())

  ABS_X = abs(X)
  ABS_Y = abs(Y)
  MIN = min(A, B)

  def COST(p, q):
    if (p-q) % 2 != 0:
      return float("inf")
    
    m = min(p, q)
    absolute = abs(p-q)
    diagonal = 2 * MIN * m
    straight = min(A+B, 4*MIN) * (absolute//2)

    return diagonal + straight
  
  ANSWER = COST(ABS_X, ABS_Y)

  ANSWER = min(ANSWER, A + COST(abs(ABS_X-1), ABS_Y))
  ANSWER = min(ANSWER, A + COST(abs(ABS_X+1), ABS_Y))
  ANSWER = min(ANSWER, B + COST(ABS_X, abs(ABS_Y-1)))
  ANSWER = min(ANSWER, B + COST(ABS_X, abs(ABS_Y+1)))

  print(ANSWER)