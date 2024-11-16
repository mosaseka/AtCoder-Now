N = str(input())
A = 0
B = 0
C = 0

for i in range(len(N)):
  if N[i] == "1":
    A += 1
  elif N[i] == "2":
    B += 1
  elif N[i] == "3":
    C += 1

if A == 1 and B == 2 and C == 3:
  print("Yes")
else:
  print("No")