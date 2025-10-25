from collections import defaultdict

N = int(input())
A_LIST = list(map(int, input().split()))
ANSWER = 0

RIGHT = defaultdict(int)
for i in range(N):
  RIGHT[A_LIST[i]] += 1

LEFT = defaultdict(int)

for j in range(N):
  RIGHT[A_LIST[j]] -= 1
  
  if 0 < j < N - 1:
    ALL_VALUES = set(A_LIST)
    for VALUE in ALL_VALUES:
      if VALUE != A_LIST[j]:
        ANSWER += LEFT[VALUE] * RIGHT[VALUE]
    
    LEFT_COUNT = j
    LEFT_SAME = LEFT[A_LIST[j]]
    LEFT_DIFF = LEFT_COUNT - LEFT_SAME
    ANSWER += LEFT_SAME * (N - j - 1 - RIGHT[A_LIST[j]])
    ANSWER += LEFT_DIFF * RIGHT[A_LIST[j]]
  
  LEFT[A_LIST[j]] += 1

print(ANSWER)