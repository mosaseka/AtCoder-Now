N = int(input())
S = str(input())

ANSWER = 0

if N == 1:
  if S[0] == "x":
    print(1)
  else:
    print(0)
  exit()

for i in range(N):
  if i == 0:
    if S[i] == "x" and S[i+1] == "x":
      ANSWER += 1
  elif i == N-1:
    if S[i] == "x" and S[i-1] == "x":
      ANSWER += 1
  else:
    if S[i] == "x" and S[i-1] == "x" and S[i+1] == "x":
      ANSWER += 1

print(ANSWER)