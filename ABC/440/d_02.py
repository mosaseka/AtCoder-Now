from bisect import bisect_left

N, Q = map(int, input().split())
A_LIST = list(map(int, input().split()))
XY_LIST = [list(map(int, input().split())) for _ in range(Q)]
A_SET = set(A_LIST)

A_LIST.sort()

for X, Y in XY_LIST:
  LEFT = X - 1
  RIGHT = X + Y + N
  
  while RIGHT - LEFT > 1:
    MID = (LEFT + RIGHT) // 2
    COUNT = bisect_left(A_LIST, MID) - bisect_left(A_LIST, X)
    TOTAL = MID - X + 1
    ROSS = TOTAL - COUNT
    if ROSS >= Y:
      RIGHT = MID
    else:
      LEFT = MID
  
  ANSWER = RIGHT
  while ANSWER in A_SET:
    ANSWER += 1

  print(ANSWER)