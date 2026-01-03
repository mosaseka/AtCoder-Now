from bisect import bisect_left

N = int(input())
AB_LIST = [tuple(map(int, input().split())) for i in range(N)]
DP = []

AB_LIST.sort(key=lambda x: (x[0], -x[1]))

for i in range(N):
  A, B = AB_LIST[i]
  CHECK = bisect_left(DP, B)
  if CHECK == len(DP):
    DP.append(B)
  else:
    DP[CHECK] = B

print(len(DP))