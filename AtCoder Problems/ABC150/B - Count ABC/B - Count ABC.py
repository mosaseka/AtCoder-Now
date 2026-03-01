N = int(input())
S = str(input())

ANSWER = 0

for i in range(N-2):
  if S[i] + S[i+1] + S[i+2] == "ABC":
    ANSWER += 1

print(ANSWER)