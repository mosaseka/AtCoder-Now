from collections import Counter

N, K = map(int, input().split())
S = str(input())
COUNTER = Counter()
ANSWER_LIST = []

for i in range(N - K + 1):
  SUBSTRING = S[i:i + K]
  COUNTER[SUBSTRING] += 1

MAX_COUNT = max(COUNTER.values())

for s, count in COUNTER.items():
  if count == MAX_COUNT:
    ANSWER_LIST.append(s)

ANSWER_LIST.sort()

print(MAX_COUNT)

for s in ANSWER_LIST:
  print(s)