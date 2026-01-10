from bisect import bisect_left, bisect_right

N, Q = map(int, input().split())
A_LIST = list(map(int, input().split()))
XY_LIST = [list(map(int, input().split())) for _ in range(Q)]

A_LIST.sort()

for X, Y in XY_LIST:
  LEFT = X - 1
  RIGHT  = X + Y + N

  while RIGHT - LEFT > 1:
    MID = (LEFT + RIGHT) // 2
    COUNT = bisect_right(A_LIST, MID) - bisect_left(A_LIST, X)
    MISSING = (MID - X + 1) - COUNT
    if MISSING >= Y:
      RIGHT = MID
    else:
      LEFT = MID
      
  print(RIGHT)