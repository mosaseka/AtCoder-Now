N = int(input())
QR_LIST = [list(map(int,input().split())) for i in range(N)]
Q = int(input())
CHECK = 0

for i in range(Q):
  T,D = map(int,input().split())
  if D % QR_LIST[T-1][0] == QR_LIST[T-1][1]:
    print(D)
  else:
    CHECK = D + (QR_LIST[T-1][1] - D % QR_LIST[T-1][0])
    if CHECK < D:
      CHECK += QR_LIST[T-1][0]
    print(CHECK)