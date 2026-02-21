N = int(input())
A_LIST = list(map(int, input().split()))

DP = {}

for a in A_LIST:
  DP[a] = DP.get(a-1, 0) + 1

print(max(DP.values()))