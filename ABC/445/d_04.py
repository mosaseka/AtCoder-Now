from collections import defaultdict

H, W, N = map(int, input().split())
HW_LIST = [list(map(int, input().split())) for _ in range(N)]

ORD_H = sorted(range(N), key=lambda x: -HW_LIST[x][0])
ORD_W = sorted(range(N), key=lambda x: -HW_LIST[x][1])

ANS_R = [0] * N
ANS_C = [0] * N
USED = [False] * N
ITH = 0
ITW = 0

for _ in range(N):
  while USED[ORD_H[ITH]]:
    ITH += 1
  while USED[ORD_W[ITW]]:
    ITW += 1
  if HW_LIST[ORD_H[ITH]][0] == H:
    I = ORD_H[ITH]
  else:
    I = ORD_W[ITW]
  ANS_R[I] = H - HW_LIST[I][0] + 1
  ANS_C[I] = W - HW_LIST[I][1] + 1
  USED[I] = True
  if HW_LIST[I][0] == H:
    W -= HW_LIST[I][1]
  else:
    H -= HW_LIST[I][0]

print('\n'.join(f"{ANS_R[i]} {ANS_C[i]}" for i in range(N)))