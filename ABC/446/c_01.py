from collections import deque

T = int(input())

for _ in range(T):
  N, D = map(int, input().split())
  A_LIST = list(map(int, input().split()))
  B_LIST = list(map(int, input().split()))

  DEQUE = deque()

  for i in range(N):
    DAY = i+1
    DEQUE.append([DAY, A_LIST[i]])

    USE = B_LIST[i]
    while USE > 0:
      if DEQUE[0][1] <= USE:
        USE -= DEQUE[0][1]
        DEQUE.popleft()
      else:
        DEQUE[0][1] -= USE
        USE = 0
    
    while DEQUE and (DAY - DEQUE[0][0]) >= D:
      DEQUE.popleft()
  
  ANSWER = 0
  for i in DEQUE:
    ANSWER += i[1]
  print(ANSWER)