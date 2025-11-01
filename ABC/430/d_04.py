from sortedcontainers import SortedList
N = int(input())
X = list(map(int, input().split()))

A = SortedList([0, X[0]])
ANS = X[0] * 2
print(ANS)
for i in range(1, N):
  INDEX = A.bisect_left(X[i])
  A.add(X[i])
  RD = 10**10
  if INDEX < i + 1:
    RD = A[INDEX + 1] - X[i]
    if INDEX + 1 == i + 1:
      RND = A[INDEX + 1] - A[INDEX - 1]
    else:
      RND = min(A[INDEX + 1] - A[INDEX - 1], A[INDEX + 2] - A[INDEX + 1])
    if RD < RND:
      ANS -= RND - RD
  LD = X[i] - A[INDEX - 1]
  if INDEX == 1:
    LND = A[INDEX + 1] - A[INDEX - 1]
  elif INDEX == i + 1:
    LND = A[INDEX - 1] - A[INDEX - 2]
  else:
    LND = min(A[INDEX + 1] - A[INDEX - 1], A[INDEX - 1] - A[INDEX - 2])
  if LD < LND:
    ANS -= LND - LD
  ANS += min(LD, RD)
  print(ANS)
