N, M = map(int, input().split())
S = [list(map(str, input())) for i in range(N)]
SET = set()
CHECK = []

for i in range(N - M + 1):
  for j in range(N - M + 1):
    CHECK = []
    for k in range(i, i + M):
      for l in range(j, j + M):
        CHECK.append(S[k][l])
    SET.add(tuple(CHECK))

print(len(SET))