N, K = map(int, input().split())
S = input()

Q = [i for i, c in enumerate(S) if c == "?"]
M = len(Q)

X = []

for i in range(1 << M):
  T = list(S)
  for j in range(M):
    T[Q[j]] = "o" if (i >> j) & 1 else "."

  OK = True
  CNT = 0
  PREV = False
  for c in T:
    if c == "o":
      if PREV:
        OK = False
        break
      CNT += 1
      PREV = True
    else:
      PREV = False

  if OK and CNT == K:
    X.append(T)

T = ""
for i in range(N):
  CH = set(x[i] for x in X)
  if CH == {"o"}:
    T += "o"
  elif CH == {"."}:
    T += "."
  else:
    T += "?"

print(T)