S = str(input())

ANSWER = 0
NOW = 0

for i, char in enumerate(S):
  if i == 0 or S[i] == S[i-1]:
    NOW = 1
  else:
    NOW += 1
  
  ANSWER = (ANSWER + NOW) % 998244353

print(ANSWER)