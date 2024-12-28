K = int(input())
S = str(input())
T = str(input())

S_LEN = len(S)
T_LEN = len(T)

if S == T:
  print("Yes")
  exit()

if abs(S_LEN - T_LEN) > 1:
  print("No")
  exit()

if S_LEN == T_LEN:
  COUNT = sum(1 for i in range(S_LEN) if S[i] != T[i])
  print("Yes" if COUNT == 1 else "No")
elif S_LEN < T_LEN:
  for i in range(S_LEN):
    if S[:i] == T[:i] and S[i:] == T[i+1:]:
      print("Yes")
      exit()
  print("No")
else:
  for i in range(T_LEN):
    if S[:i] == T[:i] and S[i+1:] == T[i:]:
      print("Yes")
      exit()
  print("No")