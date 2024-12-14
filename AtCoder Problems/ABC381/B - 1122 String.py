from collections import Counter

S = str(input())
S_COUNT = list(Counter(S).values())

#print(S_COUNT)

if len(S) % 2 == 1:
  print("No")
  exit()

for i in range(len(S)):
  if 1 <= i+1 <= len(S) // 2:
    if S[2*i - 1] != S[2*i - 2]:
      print("No")
      exit()

for i in range(len(S_COUNT)):
  if S_COUNT[i] != 2:
    print("No")
    exit()

print("Yes")