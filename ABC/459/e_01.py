MOD = 998244353

def COMB(N, K, INVERSE):
  CHECK = N % MOD
  if CHECK < K:
    return 0
  
  NUM=  1
  for i in range(K):
    NUM = NUM * (CHECK-i) % MOD
  
  return NUM * INVERSE[K] % MOD

N = int(input())
P_LIST = list(map(int, input().split()))
C_LIST = list(map(int, input().split()))
D_LIST = list(map(int, input().split()))

CHILDREN = [[] for i in range(N)]

for i, p in enumerate(P_LIST, start=1):
  CHILDREN[p-1].append(i)

ORDER = [0]
for v in ORDER:
  for to in CHILDREN[v]:
    ORDER.append(to)

MAX = max(D_LIST)

FACT = [1] * (MAX+1)
INV_FACT = [1] * (MAX+1)

for i in range(1, MAX+1):
  FACT[i] = FACT[i-1] * i % MOD

INV_FACT[MAX] = pow(FACT[MAX], MOD-2, MOD)

for i in range(MAX, 0, -1):
  INV_FACT[i-1] = INV_FACT[i] * i % MOD

SUB_C = C_LIST[:]
SUB_D = D_LIST[:]

ANSWER = 1

for v in reversed(ORDER):
  for to in CHILDREN[v]:
    SUB_C[v] += SUB_C[to]
    SUB_D[v] += SUB_D[to]
  
  if SUB_D[v] > SUB_C[v]:
    print(0)
    exit()
  
  CAN = SUB_C[v] - SUB_D[v] + D_LIST[v]

  ANSWER *= COMB(CAN, D_LIST[v], INV_FACT)
  ANSWER %= MOD

print(ANSWER)