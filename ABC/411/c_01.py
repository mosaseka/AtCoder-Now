N, Q = map(int, input().split())
A_LIST = list(map(int, input().split()))
COLOR = [0] * N # 0:白, 1:黒
BLACK = 0
LEFT = 0
RIGHT = 0

for i in A_LIST:
  INDEX = i - 1
  BEFORE = COLOR[INDEX]
  COLOR[INDEX] ^= 1
  AFTER = COLOR[INDEX]

  if INDEX > 0:
    LEFT = COLOR[INDEX-1]
  else:
    LEFT = 0
  if INDEX < N-1:
    RIGHT = COLOR[INDEX+1]
  else:
    RIGHT = 0

  if AFTER == 1:
    if LEFT == 0 and RIGHT == 0:
      BLACK += 1
    if LEFT == 1 and RIGHT == 1:
      BLACK -= 1
  else:
    if LEFT == 0 and RIGHT == 0:
      BLACK -= 1
    if LEFT == 1 and RIGHT == 1:
      BLACK += 1

  print(BLACK)