from collections import deque

N = int(input())
A_LIST = list(map(int, input().split()))
DEQUE = deque()

for a in A_LIST:
  DEQUE.append(a)
  if len(DEQUE) >= 4 and DEQUE[-1] == DEQUE[-2] == DEQUE[-3] == DEQUE[-4]:
    DEQUE.pop()
    DEQUE.pop()
    DEQUE.pop()
    DEQUE.pop()
    
print(len(DEQUE))