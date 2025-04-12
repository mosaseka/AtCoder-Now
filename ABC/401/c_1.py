from collections import deque

N, K = map(int, input().split())
DEQ = deque([1] * K)
SUM = K
MOD = 10**9

for i in range(N + 1 - K):
  NEW = SUM % MOD
  DEQ.append(NEW)
  SUM -= DEQ.popleft()
  SUM += NEW 

print(DEQ[-1] % MOD)