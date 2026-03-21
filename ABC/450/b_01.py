N = int(input())
C = [[0] * N for _ in range(N)]

for i in range(N - 1):
  C_LIST = list(map(int, input().split()))
  for d, COST in enumerate(C_LIST, start=1):
    J = i + d
    C[i][J] = COST

OK = False
for a in range(N):
  for b in range(a + 1, N):
    for c in range(b + 1, N):
      if C[a][b] + C[b][c] < C[a][c]:
        OK = True
        break
    if OK:
      break
  if OK:
    break

if OK:
  print("Yes")
else:
  print("No")