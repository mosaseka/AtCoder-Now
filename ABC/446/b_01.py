N, M = map(int, input().split())
JUICE = [i+1 for i in range(M)]

for i in range(N):
  L = int(input())
  X_LIST = list(map(int, input().split()))
  FLAG = False

  for j in range(L):
    if X_LIST[j] in JUICE:
      FLAG = True
      JUICE.remove(X_LIST[j])
      print(X_LIST[j])
      break

  if FLAG:
    pass
  else:
    print(0)      