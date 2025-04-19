from collections import defaultdict

N, M = map(int, input().split())
DISHES = []
D_DICT = defaultdict(list)

for i in range(M):
  CHECK = list(map(int, input().split()))
  INGREDIENTS = CHECK[1:]
  DISHES.append(set(INGREDIENTS))
  for j in INGREDIENTS:
    D_DICT[j].append(i)

B_LIST = list(map(int, input().split()))

DISLIKE = [len(r) for r in DISHES]
FLAG = [True] * M
COUNT = 0
ANSWER = []

for i in range(N):
  NOW = B_LIST[i]
  for j in D_DICT[NOW]:
    if FLAG[j]:
      DISLIKE[j] -= 1
      if DISLIKE[j] == 0:
        COUNT += 1
        FLAG[j] = False
  ANSWER.append(COUNT)

print(*ANSWER)