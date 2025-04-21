N = int(input())
DP = [[0] * 3 for _ in range(N + 1)]

DP[0][0], DP[0][1], DP[0][2] = 0, 0, 0

for i in range(1, N + 1):
  A, B, C = map(int, input().split())
  DP[i][0] = max(DP[i-1][1] + A, DP[i-1][2] + A)
  DP[i][1] = max(DP[i-1][0] + B, DP[i-1][2] + B)
  DP[i][2] = max(DP[i-1][0] + C, DP[i-1][1] + C)

print(max(DP[-1]))