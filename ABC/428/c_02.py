from collections import deque

Q = int(input())
STACK = deque()
COUNTER = 0
MIN_STACK = deque([0])

for i in range(Q):
  QUERY = list(map(str, input().split()))
  match QUERY[0]:
    case "1":
      STACK.append(QUERY[1])
      if QUERY[1] == '(':
        COUNTER += 1
      else:
        COUNTER -= 1
      MIN_STACK.append(min(MIN_STACK[-1], COUNTER))
    case "2":
      CHAR = STACK.pop()
      MIN_STACK.pop()
      if CHAR == '(':
        COUNTER -= 1
      else:
        COUNTER += 1
    case _:
      pass
  if COUNTER == 0 and MIN_STACK[-1] >= 0:
    print("Yes")
  else:
    print("No")