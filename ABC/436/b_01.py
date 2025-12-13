N = int(input())
ANSWER = [[0] * N for i in range(N)]
R = 0
C = (N - 1) // 2

ANSWER[R][C] = 1

for k in range(2, N**2 + 1):
  R_NEXT = (R - 1) % N
  C_NEXT = (C + 1) % N
  if ANSWER[R_NEXT][C_NEXT] == 0:
    R, C = R_NEXT, C_NEXT
  else:
    R = (R + 1) % N
  ANSWER[R][C] = k

for i in ANSWER:
  print(*i)