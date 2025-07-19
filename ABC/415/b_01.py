from collections import deque

S = str(input())
LIST = [(S[i], i+1) for i in range(len(S))]
QUEUE = deque()

for i in range(len(LIST)):
  if LIST[i][0] == "#":
    QUEUE.append(LIST[i][1])
  else:
    pass

  if len(QUEUE) == 2:
    print(str(QUEUE.popleft()) + "," + str(QUEUE.popleft()))