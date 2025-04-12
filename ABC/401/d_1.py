N, K = map(int, input().split())
S = input()

from collections import defaultdict

DP = [defaultdict(set) for _ in range(N + 1)]
DP[0][(0, False)].add("")

for i in range(N):
  for (CNT, PREV_O), SET in DP[i].items():
    for C in (".", "o") if S[i] == "?" else (S[i],):
      if C == "o":
        if PREV_O or CNT == K:
          continue
        for STR in SET:
          DP[i + 1][(CNT + 1, True)].add(STR + "o")
      else:
        for STR in SET:
          DP[i + 1][(CNT, False)].add(STR + ".")

X = set()
for (CNT, PREV_O), SET in DP[N].items():
  if CNT == K:
    X |= SET

T = ""
for i in range(N):
  CHARS = set(STR[i] for STR in X)
  if CHARS == {"."}:
    T += "."
  elif CHARS == {"o"}:
    T += "o"
  else:
    T += "?"

print(T)
