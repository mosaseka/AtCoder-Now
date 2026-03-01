S = str(input())

N = len(S)

RES = [0] * N
DIV = [0]

i = 0
while i < N:
  j = i
  while j < N and S[i] == S[j]:
    j += 1
  DIV.append(j)

  if S[i] == "L":
    A = DIV[-2] - DIV[-3]
    B = DIV[-1] - DIV[-2]
    RES[DIV[-2] - 1] = (A + 1) // 2 + B // 2
    RES[DIV[-2]] = A // 2 + (B + 1) // 2

  i = j

print(*RES)