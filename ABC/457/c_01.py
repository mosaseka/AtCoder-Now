N, K = map(int, input().split())

A_LIST = []

for _ in range(N):
  CHECK = list(map(int, input().split()))
  A_LIST.append(CHECK[1:])

C_LIST = list(map(int, input().split()))

for i in range(N):
  LEN = len(A_LIST[i]) * C_LIST[i]

  if K > LEN:
    K -= LEN
  else:
    print(A_LIST[i][(K-1)%len(A_LIST[i])])
    exit()