from decimal import Decimal

X, Y = map(int, input().split())
A_LIST = [i+1 for i in range(6)]
B_LIST = [i+1 for i in range(6)]
ANSWER = 0

for i in range(6):
  for j in range(6):
    if A_LIST[i] + B_LIST[j] >= X or abs(A_LIST[i] - B_LIST[j]) >= Y:
      ANSWER += 1

print(Decimal(ANSWER) / Decimal(36))