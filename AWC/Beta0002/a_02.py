N, K = map(int, input().split())
A_LIST = list(map(int, input().split()))

A_SET = set(A_LIST)

if K not in A_SET:
  print(-1)
else:
  print(A_LIST.index(K) + 1)