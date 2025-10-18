S = str(input())
S_LIST = list(S)

S_LIST.sort()

if S_LIST[0] != S_LIST[1]:
  print(S_LIST[0])
else:
  print(S_LIST[2])