N = int(input())

A_LIST = []

for _ in range(N):
  CHECK = list(map(int, input().split()))
  A_LIST.append(CHECK[1:])

X, Y = map(int, input().split())

print(A_LIST[X - 1][Y - 1])