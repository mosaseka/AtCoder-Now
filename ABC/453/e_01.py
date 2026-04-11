def nCr(n, r):
  if r < 0 or r > n:
    return 0
  return (FACT[n] * FACT_INV[r] * FACT_INV[n-r]) % MOD

N = int(input())
LR_LIST = [tuple(map(int, input().split())) for _ in range(N)]

MOD = 998244353

FACT = [1] * (N+1)
for i in range(1, N+1):
  FACT[i] = (FACT[i-1] * i) % MOD

FACT_INV = [1] * (N+1)
FACT_INV[N] = pow(FACT[N], MOD-2, MOD)
for i in range(N, 0, -1):
  FACT_INV[i-1] = (FACT_INV[i] * i) % MOD

AOK = [0] * N
BOK = [0] * N

M = [[0, 0], [0, 0]]
M[0][0] = N

CAND = [[] for _ in range(N+2)]
L = [0] * N
R = [0] * N

for index, (l, r) in enumerate(LR_LIST):
  L[index] = l
  R[index] = r

  CAND[l].append(index)
  if r + 1 <= N:
    CAND[r+1].append(index)
  
  t1 = N - l + 1
  t2 = N - r
  if 1 <= t1 <= N:
    CAND[t1].append(index)
  if 1 <= t2 <= N:
    CAND[t2].append(index)

ANSWER = 0

for i in range(1, N):
  for z in CAND[i]:
    M[AOK[z]][BOK[z]] -= 1

    AOK[z] = 1 if L[z] <= i <= R[z] else 0
    ni = N - i
    BOK[z] = 1 if L[z] <= ni <= R[z] else 0

    M[AOK[z]][BOK[z]] += 1
  
  if M[0][0] == 0 and M[1][0] <= i and M[0][1] <= (N - i):
    ANSWER = (ANSWER + nCr(M[1][1], i - M[1][0])) % MOD

print(ANSWER)