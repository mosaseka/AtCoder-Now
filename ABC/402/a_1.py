S = str(input())
ANSWER = ""

for i in range(len(S)):
  if S[i] == S[i].upper():
    ANSWER += S[i]

print(ANSWER)