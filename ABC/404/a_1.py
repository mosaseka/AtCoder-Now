S = input()
CHECK = "qwertyuiopasdfghjklzxcvbnm"

for i in CHECK:
  if i not in S:
    print(i)
    exit()