N = int(input())
A_LIST = list(map(int,input().split()))
CHECK = 0

for i in range(N):
  if i == 0:
    pass
  elif i == 1:
    CHECK = A_LIST[i] / A_LIST[i-1]
  else:
    if A_LIST[i-1] * CHECK == A_LIST[i]:
      pass
    else:
      print("No")
      exit()

print("Yes")