K = int(input())
S = str(input())
T = str(input())

S_LEN = len(S)
T_LEN = len(T)

if S == T:
  print("Yes")
  exit()

if S_LEN == T_LEN:
  COUNT = 0
  for i in range(S_LEN):
    if S[i] != T[i]:
      COUNT += 1
  if COUNT == 1:
    print("Yes")
  else:
    print("No")
elif S_LEN < T_LEN:
  for i in range(len(S)):
    if S[:i] == T[:i] and S[i+1:] == T[i+2:]:
      print("Yes")
      exit()
  print("No")
elif S_LEN > T_LEN:
  for i in range(len(S)):
    if S[:i] == T[:i] and S[i+2:] == T[i+1:]:
      print("Yes")
      exit()
  print("No")