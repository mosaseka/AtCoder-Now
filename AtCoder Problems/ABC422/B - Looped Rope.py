H, W = map(int, input().split())
GLID = ["." * (W + 2)] + ["." + str(input()) + "." for _ in range(H)] + ["." * (W + 2)]

for i in range(1, H + 1):
  for j in range(1, W + 1):
    COUNT = 0
    if GLID[i-1][j] == "#":
      COUNT += 1
    if GLID[i][j-1] == "#":
      COUNT += 1
    if GLID[i+1][j] == "#":
      COUNT += 1
    if GLID[i][j+1] == "#":
      COUNT += 1
    
    if GLID[i][j] == "#" and COUNT != 2 and COUNT != 4:
      print("No")
      exit()

print("Yes")