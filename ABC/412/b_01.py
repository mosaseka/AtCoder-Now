S = input()
T = input()

T_SET = set(T)

for i in range(1, len(S)):
  if S[i].isupper():
    if S[i-1] not in T_SET:
      print("No")
      exit()

print("Yes")