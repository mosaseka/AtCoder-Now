N, M, K = map(int, input().split())
A_LIST = list(map(int, input().split()))
B_LIST = list(map(int, input().split()))

COUNT = 0
SUM = 0

for b in B_LIST:
  CHECK = A_LIST[b - 1]
  if CHECK < K:
    COUNT += 1
    SUM += CHECK

print(COUNT, SUM)