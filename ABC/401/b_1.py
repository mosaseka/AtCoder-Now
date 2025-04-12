N = int(input())
LOGIN = False
COUNT = 0

for i in range(N):
  S = str(input())
  if S == "login":
    LOGIN = True
  elif S == "logout":
    LOGIN = False
  elif S == "public":
    pass
  elif S == "private":
    if LOGIN:
      pass
    else:
      COUNT += 1

print(COUNT)