S = str(input())
ANSWER = 0

for i in range(len(S)):
  if S[i] == "i" or S[i] =="j":
    ANSWER += 1

print(ANSWER)