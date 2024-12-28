K = int(input())
S = list(map(str,input()))
T = list(map(str,input()))

for i in range(2):
  while len(S) and len(T) and S[-1] == T[-1]:
    S.pop()
    T.pop()
  S = S[::-1]
  T = T[::-1]

if len(S) <= 1 and len(T) <= 1:
  print("Yes")
else:
  print("No")