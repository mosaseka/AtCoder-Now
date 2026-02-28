def SEGMENT(STRING):
  SEG = []
  COUNT = 0
  for char in STRING:
    if char == "A":
      COUNT += 1
    else:
      SEG.append(COUNT)
      COUNT = 0
  
  SEG.append(COUNT)
  return SEG

S = str(input())
T = str(input())

S_CHECK = ""
T_CHECK = ""

for i in range(len(S)):
  if S[i] != "A":
    S_CHECK += S[i]

for i in range(len(T)):
  if T[i] != "A":
    T_CHECK += T[i]

if S_CHECK != T_CHECK:
  print(-1)
  exit()

S_SEG = SEGMENT(S)
T_SEG = SEGMENT(T)

ANSWER = 0
for s, t in zip(S_SEG, T_SEG):
  ANSWER += abs(s - t)
  
print(ANSWER)