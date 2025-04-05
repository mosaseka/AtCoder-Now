A = int(input())

for i in range(400):
  if A * (i+1) == 400:
    print(i+1)
    exit()

print(-1)