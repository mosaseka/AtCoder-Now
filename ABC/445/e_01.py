def Eratosthenes(n):
  IS_PRIME = [True] * (n + 1)
  IS_PRIME[0] = IS_PRIME[1] = False
  for i in range(2, int(n ** 0.5) + 1):
    if IS_PRIME[i]:
      for j in range(i * i, n + 1, i):
        IS_PRIME[j] = False
  return [i for i in range(2, n + 1) if IS_PRIME[i]]

MOD = 998244353
PRIMES = Eratosthenes(3162)

def FACTORIZE(n):
  FACTORS = {}
  for P in PRIMES:
    if P * P > n:
      break
    if n % P == 0:
      E = 0
      while n % P == 0:
        n //= P
        E += 1
      FACTORS[P] = E
  if n > 1:
    FACTORS[n] = 1
  return FACTORS

T = int(input())
for _ in range(T):
  N = int(input())
  A = list(map(int, input().split()))

  FACTS = [FACTORIZE(a) for a in A]

  PRIME_INFO = {}
  for f in FACTS:
    for p, e in f.items():
      if p not in PRIME_INFO:
        PRIME_INFO[p] = (e, 0, 1)
      else:
        M1, M2, CNT = PRIME_INFO[p]
        if e > M1:
          PRIME_INFO[p] = (e, M1, 1)
        elif e == M1:
          PRIME_INFO[p] = (M1, M2, CNT + 1)
        else:
          if e > M2:
            PRIME_INFO[p] = (M1, e, CNT)

  LCM_ALL = 1
  for p, (M1, M2, CNT) in PRIME_INFO.items():
    LCM_ALL = LCM_ALL * pow(p, M1, MOD) % MOD

  ANS = []
  for i in range(N):
    CORRECTION = 1
    for p, e in FACTS[i].items():
      M1, M2, CNT = PRIME_INFO[p]
      if e == M1 and CNT == 1:
        CORRECTION = CORRECTION * pow(p, M1 - M2, MOD) % MOD
    ANS.append(LCM_ALL * pow(CORRECTION, MOD - 2, MOD) % MOD)

  print(*ANS)