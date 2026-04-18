from collections import deque

def COMP(S):
  DEQ = deque()
  for char in S:
    DEQ.append(char)

    while (len(DEQ) >= 4 and DEQ[-4] == "(" and DEQ[-3] == "x" and DEQ[-2] == "x" and DEQ[-1] == ")"):
      DEQ.pop()
      DEQ.pop()
      DEQ.pop()
      DEQ.pop()
      DEQ.append("x")
      DEQ.append("x")
  
  return "".join(DEQ)

T = int(input())

for _ in range(T):
  A = str(input())
  B = str(input())

  CHECK = COMP(A)

  if CHECK == COMP(B):
    print("Yes")
    continue

  print("No")