N = str(input())
CHECKED = set()
CHECK = 0

while True:
  for i in range(len(N)):
    CHECK += (int(N[i]))**2
  if CHECK == 1:
    print("Yes")
    exit()
  elif CHECK in CHECKED:
    print("No")
    exit()
  else:
    CHECKED.add(CHECK)
    N = str(CHECK)
    CHECK = 0