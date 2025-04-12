N, K = map(int, input().split())
S = input()

DP1 = [[[False] * 2 for _ in range(K + 2)] for _ in range(N + 1)]
DP1[0][0][0] = True

for i in range(N):
  for k in range(K + 1):
    for p in range(2):
      if not DP1[i][k][p]:
        continue
      for C in (".", "o") if S[i] == "?" else (S[i],):
        if C == ".":
          DP1[i + 1][k][0] = True
        elif C == "o" and p == 0 and k + 1 <= K:
          DP1[i + 1][k + 1][1] = True

DP2 = [[[False] * 2 for _ in range(K + 2)] for _ in range(N + 2)]
DP2[N][0][0] = True

for i in range(N - 1, -1, -1):
  for k in range(K + 1):
    for p in range(2):
      if not DP2[i + 1][k][p]:
        continue
      for C in (".", "o") if S[i] == "?" else (S[i],):
        if C == ".":
          DP2[i][k][0] = True
        elif C == "o" and p == 0 and k + 1 <= K:
          DP2[i][k + 1][1] = True

T = ""
for i in range(N):
  DOT = False
  OOO = False
  for k in range(K + 1):
    for p1 in range(2):
      if not DP1[i][k][p1]:
        continue
      for p2 in range(2):
        if not DP2[i + 1][K - k][p2]:
          continue
        if S[i] in ".?":
          DOT = True
        if S[i] in "o?" and p1 == 0 and p2 == 0:
          OOO = True
  if DOT and OOO:
    T += "?"
  elif DOT:
    T += "."
  else:
    T += "o"

print(T)
