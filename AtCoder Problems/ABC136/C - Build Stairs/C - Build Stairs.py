N = int(input())
H = list(map(int, input().split()))

i = N - 2
while i >= 0:
  if H[i] > H[i+1] + 1:
    print("No")
    exit()
  elif H[i] == H[i+1] + 1:
    H[i] -= 1
  
  i -= 1

print("Yes")