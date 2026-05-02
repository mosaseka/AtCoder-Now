X = int(input())

for i in range(1, 7):
  for j in range(1, 7):
    for k in range(1, 7):
      if i + j + k == X:
        print("Yes")
        exit()

print("No")