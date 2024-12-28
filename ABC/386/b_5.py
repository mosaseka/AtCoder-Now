S = list(map(int,input()))
COUNT = 0
INDEX = 0

while INDEX < len(S):
  if S[INDEX] != 0:
    INDEX += 1
    COUNT += 1
  else:
    if INDEX + 1 < len(S) and S[INDEX + 1] == 0:
      INDEX += 2
      COUNT += 1
    else:
      INDEX += 1
      COUNT += 1

print(COUNT)