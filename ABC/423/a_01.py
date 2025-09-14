X, C = map(int, input().split())

LEFT, RIGHT = 0, X // 1000 + 1

while RIGHT - LEFT > 1:
  MID = (LEFT + RIGHT) // 2
  TOTAL = MID * 1000 + MID * C
  
  if TOTAL <= X:
    LEFT = MID
  else:
    RIGHT = MID

MAX = LEFT * 1000
print(MAX)