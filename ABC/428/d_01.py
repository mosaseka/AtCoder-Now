import math

def floor_sqrt(X):
  Y = int(math.sqrt(X))
  while Y * Y > X:
    Y -= 1
  while (Y + 1) * (Y + 1) <= X:
    Y += 1
  return Y

T = int(input())

for i in range(T):
  C, D = map(int, input().split())
  ANS = 0
  
  XMIN = 1
  XMAX = 9
  CSHIFT = 10
  
  while XMIN <= C + D:
    L = max(XMIN, C + 1)
    R = min(XMAX, C + D)
    
    if L <= R:
      VL = C * CSHIFT + L
      VR = C * CSHIFT + R
      
      ANS += floor_sqrt(VR) - floor_sqrt(VL - 1)
    
    XMIN = XMIN * 10
    XMAX = (XMAX + 1) * 10 - 1
    CSHIFT *= 10
  
  print(ANS)