X = int(input())
ANSWER = 0

for i in range(9):
  for j in range(9):
    if (i+1)*(j+1) != X:
      ANSWER += (i+1)*(j+1)

print(ANSWER)