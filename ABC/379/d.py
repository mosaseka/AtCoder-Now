from collections import deque

Q = int(input())
QUE = deque()
HEIGHT = [0] * (Q + 1)
CHECK = []
ANSWER = 0

for i in range(Q):
  CHECK = list(map(str, input().split()))
  if CHECK[0] == "1":
    HEIGHT[i+1] = HEIGHT[i]
    QUE.append(i)
  elif CHECK[0] == "2":
    HEIGHT[i+1] = HEIGHT[i] + int(CHECK[1])
  elif CHECK[0] == "3":
    HEIGHT[i+1] = HEIGHT[i]
    ANSWER = 0
    while QUE:
      if HEIGHT[i+1] - HEIGHT[QUE[0]] >= int(CHECK[1]):
        QUE.popleft()
        ANSWER += 1
      else:
        break
    print(ANSWER)