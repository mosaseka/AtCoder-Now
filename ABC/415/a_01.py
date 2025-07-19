N = int(input())
A_SET = set(map(int,input().split()))
X = int(input())

if X in A_SET:
  print("Yes")
else:
  print("No")