N = int(input())
S = str(input())

A_POSITIONS = []
for i in range(2 * N):
  if S[i] == 'A':
    A_POSITIONS.append(i + 1)

COST1 = 0 #ABABAB
COST2 = 0 #BABABA

for k in range(N):
  CURRENT_POS = A_POSITIONS[k]
  
  TARGET_POS1 = 2 * k + 1
  COST1 += abs(CURRENT_POS - TARGET_POS1)
  
  TARGET_POS2 = 2 * k + 2
  COST2 += abs(CURRENT_POS - TARGET_POS2)

print(min(COST1, COST2))