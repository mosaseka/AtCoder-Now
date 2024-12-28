from collections import deque

S = deque(map(int,input()))
COUNT = 0

while len(S) != 0:
  if S[0] != 0:
    S.popleft()
    COUNT += 1
  else:
    if len(S) == 1:
      S.popleft()
      COUNT += 1
    elif S[1] == 0:
      S.popleft()
      S.popleft()
      COUNT += 1

print(COUNT)