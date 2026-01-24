N, M = map(int, input().split())
AB_LIST = [tuple(map(int, input().split())) for _ in range(M)]
ANSWER = []
CONFLICT = [set() for _ in range(N + 1)]

for a, b in AB_LIST:
  CONFLICT[a].add(b)
  CONFLICT[b].add(a)

for i in range(1, N + 1):
  CHECK = N - 1 - len(CONFLICT[i])
  if CHECK < 3:
    ANSWER.append(0)
  else:
    ANSWER.append(CHECK * (CHECK - 1) * (CHECK - 2) // 6)
  
print(*ANSWER)