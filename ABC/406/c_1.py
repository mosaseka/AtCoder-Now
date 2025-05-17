N = int(input())
P = list(map(int, input().split()))
ANSWER = 0

for l in range(N):
  for r in range(l + 4, N + 1):  # 長さ4以上のみ
    CHECK = P[l:r]
    ALPHA = 0
    BETA = 0
    if CHECK[0] >= CHECK[1]:
      continue
    for i in range(1, len(CHECK)-1):
      if CHECK[i-1] < CHECK[i] > CHECK[i+1]:
        ALPHA += 1
      if CHECK[i-1] > CHECK[i] < CHECK[i+1]:
        BETA += 1
    if ALPHA == 1 and BETA == 1:
      ANSWER += 1

print(ANSWER)