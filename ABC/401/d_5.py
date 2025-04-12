N, K = map(int, input().split())
S = input()

ANS = [None] * N
CNT = 0
for I in range(N):
  if S[I] == "o":
    ANS[I] = "o"
    CNT += 1
    if I > 0:
      ANS[I - 1] = "."
    if I < N - 1:
      ANS[I + 1] = "."
  elif S[I] == ".":
    ANS[I] = "."

REM = K - CNT
CNT = 0
CON = 0
L = 0
RANGES = []
for I in range(N):
  if ANS[I] == None:
    CON += 1
    if CON == 1:
      L = I
  else:
    if CON > 0:
      CNT += (CON + 1) // 2
      CON = 0
      RANGES.append((L, I))

if CON > 0:
  CNT += (CON + 1) // 2
  RANGES.append((L, N))

if REM == 0:
  for I in range(N):
    if ANS[I] == None:
      ANS[I] = "."
elif CNT > REM:
  for I in range(N):
    if ANS[I] == None:
      ANS[I] = "?"
else:
  for L, R in RANGES:
    if (R - L) & 1:
      for I in range(L, R):
        if (I - L) & 1:
          ANS[I] = "."
        else:
          ANS[I] = "o"
    else:
      for I in range(L, R):
        ANS[I] = "?"

print("".join(ANS))