K = int(input())
S = str(input())
T = str(input())

S_LEN = len(S)
T_LEN = len(T)

if S_LEN + 1 == T_LEN:
  for i in range(T_LEN):
    if S[:i] + T[i] + S[i:] == T:
      print("Yes")
      exit()
  print("No")
elif S_LEN - 1 == T_LEN:
  for i in range(S_LEN):
    if S[:i] + S[i+1:] == T:
      print("Yes")
      exit()
  print("No")
elif S_LEN == T_LEN:
  COUNT = 0
  for i in range(S_LEN):
    if S[i] != T[i]:
      COUNT += 1
    if COUNT > 1:
      print("No")
      exit()
  print("Yes")