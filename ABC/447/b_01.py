from collections import Counter

S = str(input())

COUNT = Counter(S)
MAX_COUNT = max(COUNT.values())

REMOVE = {c for c, v in COUNT.items() if v == MAX_COUNT}

ANSWER = ""
for char in S:
  if char not in REMOVE:
    ANSWER += char

print(ANSWER)