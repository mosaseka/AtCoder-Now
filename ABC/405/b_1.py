from collections import deque

N, M = map(int, input().split())
A = deque(map(int,input().split()))
SET = set(A)

for i in range(M):
  if i+1 in SET:
    pass
  else:
    print(0)
    exit()

for i in range(N):
  A.pop()
  SET = set(A)
  for j in range(M):
    if j+1 not in SET:
      print(i+1)
      exit()

