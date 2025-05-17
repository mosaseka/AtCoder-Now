A, B, C, D = map(int, input().split())

DEADLINE = A * 60 + B
SUBMIT = C * 60 + D

if SUBMIT < DEADLINE:
  print("Yes")
else:
  print("No")