from bisect import bisect_right

N = int(input())

H_LIST = [0] * N
L_LIST = [0] * N
for i in range(N):
  H, L = map(int, input().split())
  H_LIST[i] = H
  L_LIST[i] = L

Q = int(input())
T_LIST = list(map(int, input().split()))

PREFIX = H_LIST.copy()
for i in range(N-2, -1, -1):
  PREFIX[i] = max(PREFIX[i], PREFIX[i+1])

for t in T_LIST:
  INDEX = bisect_right(L_LIST, t)
  print(PREFIX[INDEX])