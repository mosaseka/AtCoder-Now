from collections import Counter

LIST = list(map(int,input().split()))
COUNT = list(Counter(LIST).items())
#print(COUNT)

if len(COUNT) != 2:
  print("No")
  exit()

if COUNT[0][1] == 3 and COUNT[1][1] == 1:
  print("Yes")
elif COUNT[0][1] == 1 and COUNT[1][1] == 3:
  print("Yes")
elif COUNT[0][1] == 2 and COUNT[1][1] == 2:
  print("Yes")
else:
  print("No")