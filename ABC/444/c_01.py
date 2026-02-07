from collections import Counter

def DIVISORS(N):
  RETURN = []
  for i in range(1, int(N**0.5)+1):
    if N % i == 0:
      RETURN.append(i)
      if i != N // i:
        RETURN.append(N // i)
  RETURN.sort()
  return RETURN

N = int(input())
A_LIST = list(map(int, input().split()))

SUM = sum(A_LIST)
SUM_DIV = DIVISORS(SUM)

A_MAX = max(A_LIST)

ANSWER = []

for L in SUM_DIV:
  if A_MAX > L:
    continue
  
  COUNT = Counter(A_LIST)
  
  FLAG = True
  for a in sorted(COUNT.keys(), reverse=True):
    if COUNT[a] == 0:
      continue
    
    if a == L:
      COUNT[a] = 0
    else:
      NEED = L - a
      if NEED == a:
        if COUNT[a] % 2 != 0:
          FLAG = False
          break
        COUNT[a] = 0
      else:
        if COUNT[NEED] < COUNT[a]:
          FLAG = False
          break
        COUNT[NEED] -= COUNT[a]
        COUNT[a] = 0
  
  if FLAG:
    ANSWER.append(L)

print(*ANSWER)