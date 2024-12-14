N,C_1, C_2 = map(str, input().split())
N = int(N)
S = str(input())
ANSWER = ""

for i in range(N):
  if S[i] != C_1:
    ANSWER += C_2
  else:
    ANSWER += C_1

print(ANSWER)