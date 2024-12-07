from collections import deque

N = int(input())
WATER = 0
TV_LIST = deque([list(map(int, input().split())) for i in range(N)])

for i in range(TV_LIST[-1][0]):
  if TV_LIST[0][0] == i+1:
    WATER += TV_LIST[0][1]
    TV_LIST.popleft()
  if len(TV_LIST) == 0:
    break
  if WATER > 0:
    WATER -= 1

print(WATER)