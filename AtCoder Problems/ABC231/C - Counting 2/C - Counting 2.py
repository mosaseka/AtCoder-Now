from bisect import bisect_left

N, Q = map(int, input().split())
A_LIST = list(map(int, input().split()))

A_LIST.sort()

for _ in range(Q):
  X = int(input())
  index = bisect_left(A_LIST, X)

  if index < 0:
    index = -(index + 1)
  
  print(N - index)