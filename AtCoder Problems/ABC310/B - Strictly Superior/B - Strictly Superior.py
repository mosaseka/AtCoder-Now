N,M = map(int,input().split())
P_LIST = []
C_LIST = []
F_LIST = []
LIST = []
ALPHA = True
BETA = True

for i in range(N):
  LIST = list(map(int,input().split()))
  P_LIST.append(LIST[0])
  C_LIST.append(LIST[1])
  F_LIST.append(LIST[2:])


for i in range(N):
  for j in range(N):
    if i == j:
      continue
    ALPHA = True
    BETA = True
    if P_LIST[i] >= P_LIST[j]:
      for k in range(len(F_LIST[i])):
        if F_LIST[i][k] not in set(F_LIST[j]):
          ALPHA = False
          break
      if P_LIST[i] > P_LIST[j] or len(F_LIST[j]) > len(F_LIST[i]):
        pass
      else:
        BETA = False
      if ALPHA and BETA:
        print("Yes")
        exit()

print("No")