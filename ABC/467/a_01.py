H, W = map(int, input().split())

H = H / 100

BMI = W / H / H

if BMI >= 25:
  print("Yes")
else:
  print("No")