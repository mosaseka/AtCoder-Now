X, Y = map(str, input().split())
OS_LIST = ["Ocelot", "Serval", "Lynx"]

if OS_LIST.index(X) >= OS_LIST.index(Y):
  print("Yes")
else:
  print("No")