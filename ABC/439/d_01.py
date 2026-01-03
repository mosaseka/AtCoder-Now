from collections import defaultdict
from bisect import bisect_left, bisect_right

N = int(input())
A_LIST = list(map(int, input().split()))
ANSWER = 0
POSITION = defaultdict(list)

for index in range(N):
  POSITION[A_LIST[index]].append(index)

for j in range(N):
  if A_LIST[j] % 5 != 0:
    continue
  
  CONST = A_LIST[j] // 5
  I_VAL = 7 * CONST
  K_VAL = 3 * CONST
  
  I_POSITIONS = POSITION[I_VAL]
  I_RIGHT = len(I_POSITIONS) - bisect_left(I_POSITIONS, j)
  K_POSITIONS = POSITION[K_VAL]
  K_RIGHT = len(K_POSITIONS) - bisect_left(K_POSITIONS, j)
  ANSWER += I_RIGHT * K_RIGHT
  
  I_LEFT = bisect_right(I_POSITIONS, j)
  K_LEFT = bisect_right(K_POSITIONS, j)
  ANSWER += I_LEFT * K_LEFT

print(ANSWER)