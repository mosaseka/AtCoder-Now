from bisect import bisect_left

N, Q = map(int, input().split())
A_LIST = list(map(int, input().split()))
XY_LIST = [list(map(int, input().split())) for _ in range(Q)]

A_LIST.sort()

for X, Y in XY_LIST:
  INDEX = bisect_left(A_LIST, X)
  CHECK_LIST = A_LIST[INDEX:]
  COUNT = 0
  NOW = X
  for a in CHECK_LIST:
    DIFF = a - NOW
    if COUNT + DIFF >= Y:
      print(NOW + (Y - COUNT - 1))
      break
    COUNT += DIFF
    NOW = a + 1
  else:
    print(NOW + (Y - COUNT - 1))