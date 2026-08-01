N = int(input())
S = str(input())

POSITION = []

for i, char in enumerate(S):
  if char == "x":
    POSITION.append(i)

for k in range(1, N+1):
  if k <= len(POSITION):
    print(POSITION[k-1]+1)
  else:
    print(N)