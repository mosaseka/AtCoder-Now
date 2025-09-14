S = str(input())

I = int(S[0])
J = int(S[-1])

if J < 8:
  print(str(I) + "-" + str(J+1))
elif I < 8 and J == 8:
  print(str(I+1) + "-1")
elif I == 8 and J == 8:
  exit()