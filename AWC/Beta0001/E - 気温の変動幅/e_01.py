from collections import deque

N, K = map(int, input().split())
H_LIST = list(map(int, input().split()))

MAX_DEQUE = deque([0 for i in range(N)])
MIN_DEQUE = deque([0 for i in range(N)])
BEST = float('-inf')

for i in range(N):
  H = H_LIST[i]

  while MAX_DEQUE and H_LIST[MAX_DEQUE[-1]] <= H:
    MAX_DEQUE.pop()
  MAX_DEQUE.append(i)

  while MIN_DEQUE and H_LIST[MIN_DEQUE[-1]] >= H:
    MIN_DEQUE.pop()
  MIN_DEQUE.append(i)

  if MAX_DEQUE and MAX_DEQUE[0] <= i - K:
    MAX_DEQUE.popleft()
  
  if MIN_DEQUE and MIN_DEQUE[0] <= i - K:
    MIN_DEQUE.popleft()
  
  if i >= K-1:
    DIFF = H_LIST[MAX_DEQUE[0]] - H_LIST[MIN_DEQUE[0]]
    if i == K-1 or DIFF > BEST:
      BEST = DIFF

print(BEST)