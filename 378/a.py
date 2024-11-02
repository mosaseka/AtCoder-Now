A_LIST = list(map(int,input().split()))
COUNT = 0
INDEX = 0

A_LIST.sort()

while INDEX < len(A_LIST) - 1:
  if A_LIST[INDEX] == A_LIST[INDEX+1]:
    del A_LIST[INDEX:INDEX+2]
    COUNT += 1
  else:
    INDEX += 1

print(COUNT)