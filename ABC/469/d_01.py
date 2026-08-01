N, M = map(int, input().split())
AB_LIST = [tuple(map(int, input().split())) for _ in range(M)]

ALPHA, BETA = AB_LIST[0]

def COUNT(V):
  AND = None

  for a, b in AB_LIST:
    if a == V or b == V:
      continue

    if AND is None:
      AND = (a, b)
    else:
      AND = [u for u in AND if u == a or u == b]
      if not AND:
        return 0
  
  if AND is None:
    return N-1
  
  return len(AND)

ANSWER = COUNT(ALPHA) + COUNT(BETA)

FLAG = True
for a, b in AB_LIST:
  if a != ALPHA and a != BETA and b != ALPHA and b != BETA:
    FLAG = False
    break

if FLAG:
  print(ANSWER-1)
else:
  print(ANSWER)