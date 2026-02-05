S = str(input())
ANSWER = 0

for i in range(len(S)):
  if S[i] == "1":
    ANSWER += 1

print(ANSWER)