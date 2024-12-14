N, M = map(int,input().split())
LIST = [False] * N
A = 0
B = ""

for i in range(M):
  A,B = map(str,input().split())
  A = int(A)
  if LIST[A-1] == False and B == "M":
    print("Yes")
    LIST[A-1] = True
  else:
    print("No")