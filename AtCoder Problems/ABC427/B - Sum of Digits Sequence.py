def f(x):
  CHECK = str(x)
  SUM = 0
  for i in range(len(CHECK)):
    SUM += int(CHECK[i])
  return SUM

N = int(input())
A = 1

for i in range(N):
  if i == 0:
    pass
  else:
    A += f(A)

print(A)