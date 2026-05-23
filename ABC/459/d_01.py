from collections import Counter

T = int(input())

for _ in range(T):
  S = str(input())
  
  LEN = len(S)

  COUNTER = Counter(S)

  if max(COUNTER.values()) > (LEN+1) // 2:
    print("No")
    continue

  CHAR_LIST = []
  for c, num in sorted(COUNTER.items(), key=lambda x: -x[1]):
    CHAR_LIST.extend([c] * num)
  
  ANSWER = [""] * LEN
  POSITION = list(range(0, LEN, 2)) + list(range(1, LEN, 2))

  for p, c in zip(POSITION, CHAR_LIST):
    ANSWER[p] = c
  
  print("Yes")
  print("".join(ANSWER))