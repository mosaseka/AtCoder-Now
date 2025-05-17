N = int(input())
P = list(map(int, input().split()))

V = []
for i in range(N - 1):
  if P[i] < P[i + 1]:
    if not V or V[-1][0] == '>':
      V.append(('<', 1))
    else:
      V[-1] = (V[-1][0], V[-1][1] + 1)
  else:
    if not V or V[-1][0] == '<':
      V.append(('>', 1))
    else:
      V[-1] = (V[-1][0], V[-1][1] + 1)

ANS = 0
for i in range(1, len(V) - 1):
  if V[i][0] == '>':
    ANS += V[i - 1][1] * V[i + 1][1]

print(ANS)