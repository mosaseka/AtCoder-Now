S = input()
T = input()

LEN = len(T)
DP = [-1] * (LEN + 1)
ANSWER = 0

for RIGHT, CHAR in enumerate(S):
  for j in range(LEN, 0, -1):
    if CHAR != T[j - 1]:
      continue
    if j == 1:
      if RIGHT > DP[1]:
        DP[1] = RIGHT
    elif DP[j - 1] > DP[j]:
      DP[j] = DP[j - 1]
  if DP[LEN] == -1:
    ANSWER += RIGHT + 1
  else:
    ANSWER += RIGHT - DP[LEN]

print(ANSWER)