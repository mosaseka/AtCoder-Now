N = int(input())
S = str(input())

if len(S) % 2 == 0:
  print("No")
  exit()

for i in range((len(S)+1) // 2 - 1):
  if S[i] != "1":
    print("No")
    exit()

if S[(len(S)+1) // 2 - 1] != "/":
  print("No")
  exit()

CHECK = S[(len(S)+1) // 2 : len(S)]
#print(CHECK)

for i in range(len(CHECK)):
  if CHECK[i] != "2":
    print("No")
    exit()

print("Yes")