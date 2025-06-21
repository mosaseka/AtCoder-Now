N, Q = map(int, input().split())

PARENT = [None]
SEG = [""]

SERVER = 0
PC = [0] * N

for i in range(Q):
  ROW = input().split()
  QUERY_TYPE = int(ROW[0])
  PC_NAME = int(ROW[1]) - 1
  if QUERY_TYPE == 1:
    PC[PC_NAME] = SERVER
  elif QUERY_TYPE == 2:
    S = ROW[2]
    NEW = len(PARENT)
    PARENT.append(PC[PC_NAME])
    SEG.append(S)
    PC[PC_NAME] = NEW
  else:
    SERVER = PC[PC_NAME]

ANS = []
CURRENT = SERVER
while CURRENT is not None:
  ANS.append(SEG[CURRENT])
  CURRENT = PARENT[CURRENT]

ANS.reverse()
print("".join(ANS))