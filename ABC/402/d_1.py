N, M = map(int, input().split())
CNT = [0] * N

for i in range(M):
  A, B = map(int, input().split())
  CNT[(A + B) % N] += 1

ANS = M * (M - 1) // 2

for E in CNT:
  ANS -= E * (E - 1) // 2

print(ANS)