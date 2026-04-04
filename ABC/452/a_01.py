M, D = map(int, input().split())
FLAG = False

if M == 1 and D == 7:
  FLAG = True
elif M == 3 and D == 3:
  FLAG = True
elif M == 5 and D == 5:
  FLAG = True
elif M == 7 and D == 7:
  FLAG = True
elif M == 9 and D == 9:
  FLAG = True

if FLAG:
  print("Yes")
else:
  print("No")