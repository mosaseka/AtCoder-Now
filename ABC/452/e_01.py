N, M = map(int, input().split())
A_LIST = list(map(int, input().split()))
B_LIST = list(map(int, input().split()))

MOD = 998244353

PREF_A = [0] * (N + 1)
WEIGHTED_A = 0
for i, A in enumerate(A_LIST, 1):
  PREF_A[i] = PREF_A[i - 1] + A
  WEIGHTED_A += i * A

BASE = (WEIGHTED_A % MOD) * (sum(B_LIST) % MOD) % MOD

SUB = 0
LIMIT = min(N, M)
for j in range(1, LIMIT + 1):
  WEIGHTED_SUM = 0
  LEFT = j
  QUOTIENT = 1
  while LEFT <= N:
    RIGHT = LEFT + j - 1
    if RIGHT > N:
      RIGHT = N
    WEIGHTED_SUM += QUOTIENT * (PREF_A[RIGHT] - PREF_A[LEFT - 1])
    QUOTIENT += 1
    LEFT += j
  SUB = (SUB + (j * B_LIST[j - 1]) % MOD * (WEIGHTED_SUM % MOD)) % MOD

print((BASE - SUB) % MOD)