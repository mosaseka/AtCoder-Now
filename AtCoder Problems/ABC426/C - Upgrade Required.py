N, Q = map(int, input().split())
PC = [0] + [1] * N
O = 1

for i in range(Q):
  X, Y = map(int, input().split())
  COUNT = 0
  while O <= X:
    COUNT += PC[O]
    PC[Y] += PC[O]
    O += 1
  print(COUNT)