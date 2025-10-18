Q = int(input())
S = ""
COUNT = 0
FLAG = True

for i in range(Q):
  QUERY = list(map(str, input().split()))
  match QUERY[0]:
    case "1":
      S += QUERY[1]
      if QUERY[1] == '(':
        COUNT += 1
      else:
        COUNT -= 1
        if COUNT < 0:
          FLAG = False
    case "2":
      if S[-1] == '(':
        COUNT -= 1
      else:
        COUNT += 1
      S = S[:-1]
      if COUNT >= 0:
        FLAG = True
      else:
        FLAG = False
    case _:
      pass
  if FLAG and COUNT == 0:
    print("Yes")
  else:
    print("No")