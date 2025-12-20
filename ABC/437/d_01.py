from bisect import bisect_right

N, M = map(int, input().split())
A_LIST = list(map(int, input().split()))
B_LIST = list(map(int, input().split()))
SUM_LIST = [0] * (M + 1)
ANSWER = 0
B_TOTAL = 0

B_LIST.sort()

for i, x in enumerate(B_LIST, 1):
  SUM_LIST[i] = SUM_LIST[i - 1] + x

B_TOTAL = SUM_LIST[-1]

for i in A_LIST:
  CHECK = bisect_right(B_LIST, i)
  LEFT_SUM = i * CHECK - SUM_LIST[CHECK]
  RIGHT_SUM = (B_TOTAL - SUM_LIST[CHECK]) - i * (M - CHECK)
  ANSWER += LEFT_SUM + RIGHT_SUM

print(ANSWER % 998244353)