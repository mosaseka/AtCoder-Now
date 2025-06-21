N, Q = map(int, input().split())
OP = [0] * Q
P = [0] * Q
S = [""] * Q

for i in range(Q):
  PARTS = input().split()
  OP[i] = int(PARTS[0])
  P[i] = int(PARTS[1])
  if OP[i] == 2:
    S[i] = PARTS[2][::-1]

ANS = ""
i = 0
for T in reversed(range(Q)):
  if OP[T] == 1:
    if i == P[T]:
      i = 0
  elif OP[T] == 2:
    if i == P[T]:
      ANS += S[T]
  else:
    if i == 0:
      i = P[T]

print(ANS[::-1])
