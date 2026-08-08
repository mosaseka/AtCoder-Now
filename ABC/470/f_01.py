from atcoder.dsu import DSU

N, M = map(int, input().split())
S = str(input())

MOD = 998244353
DSU = DSU(N)

for _ in range(M):
  A, B = map(int, input().split())
  DSU.merge(A - 1, B - 1)

FACT = [1] * (N+1)
for i in range(1, N+1):
  FACT[i] = (FACT[i-1] * i) % MOD

FACT_INV = [1] * (N+1)
FACT_INV[N] = pow(FACT[N], MOD-2, MOD)
for i in range(N, 0, -1):
  FACT_INV[i-1] = (FACT_INV[i] * i) % MOD

SIZE = [0] * N
COUNT = {}

for i, char in enumerate(S):
  R = DSU.leader(i)
  SIZE[R] += 1
  COUNT[(R, char)] = COUNT.get((R, char), 0) + 1

ANSWER = 1

for size in SIZE:
  if size:
    ANSWER = (ANSWER * FACT[size]) % MOD

FLAG = False

for c in COUNT.values():
  ANSWER = (ANSWER * FACT_INV[c]) % MOD
  if c >= 2:
    FLAG = True

if not FLAG:
  ANSWER = ANSWER * pow(2, MOD-2, MOD) % MOD

print(ANSWER)