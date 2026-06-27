S = str(input())

EAST = 0
WEST = 0

for i in range(len(S)):
  if S[i] == "E":
    EAST += 1
  elif S[i] == "W":
    WEST += 1

if EAST > WEST:
  print("East")
elif EAST < WEST:
  print("West")