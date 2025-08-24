X, Y = map(int, input().split())

MONTH = (X + Y) % 12

if MONTH == 0:
  print(12)
else:
  print(MONTH)