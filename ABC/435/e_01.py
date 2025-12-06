N, Q = map(int, input().split())
BOARD = 0

for i in range(Q):
  L, R = map(int, input().split())
  CHECK = ((1 << (R - L + 1)) - 1) << (L - 1)
  #print(bin(CHECK))
  BOARD = BOARD | CHECK
  print(N - BOARD.bit_count())