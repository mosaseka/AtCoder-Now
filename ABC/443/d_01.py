T = int(input())

for _ in range(T):
  N = int(input())
  R_LIST = list(map(int, input().split()))

  A = R_LIST[:]

  for i in range(1, N):
    A[i] = min(A[i], A[i-1] + 1)
    
  for i in range(N-2, -1, -1):
    A[i] = min(A[i], A[i+1] + 1)

  ans = sum(R_LIST) - sum(A)
  print(ans)