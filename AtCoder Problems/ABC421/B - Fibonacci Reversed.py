A_LIST = [0] * 10
A_LIST[0], A_LIST[1] = map(int, input().split())

for i in range(2, 10):
  CHECK = str(A_LIST[i-2] + A_LIST[i-1])
  A_LIST[i] = int(CHECK[::-1])

print(A_LIST[-1])