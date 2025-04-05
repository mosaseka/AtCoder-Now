N, M = map(int,input().split())

if N == 1:
  print(M + 1)
else:
  CHECK =  (N**(M+1) - 1) // (N - 1)
  if CHECK > 10**9:
    print("inf")
  else:
    print(CHECK)
  