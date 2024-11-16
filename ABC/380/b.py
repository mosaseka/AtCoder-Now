S = str(input())
A_LIST = []
COUNT = 0

for i in range(len(S)):
  if i == 0:
    pass
  else:
    if S[i] == "|":
      A_LIST.append(COUNT)
      COUNT = 0
    else:
      COUNT += 1

print(*A_LIST)