from bisect import bisect_left

N = int(input())
AB_LIST = [tuple(map(int, input().split())) for i in range(N)]
DP = []

AB_LIST.sort(key=lambda x: x[1])

for i in range(N):
  A, B = AB_LIST[i]
  CHECK = bisect_left(DP, A)
  if CHECK == len(DP):
    DP.append(A)
  else:
    DP[CHECK] = A

print(len(DP))