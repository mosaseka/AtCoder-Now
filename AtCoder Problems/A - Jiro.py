AB, AC, BC = map(str, input().split())

if AB != AC:
  print("A")
elif AB == BC:
  print("B")
else:
  print("C")