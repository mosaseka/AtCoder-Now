N = int(input())
P = list(map(int, input().split()))
IS_PEAK = [0] * N
IS_VALLEY = [0] * N
PEAK_SUM = [0] * (N + 1)
VALLEY_SUM = [0] * (N + 1)
ANSWER = 0

for i in range(1, N - 1):
  if P[i - 1] < P[i] > P[i + 1]:
    IS_PEAK[i] = 1
  elif P[i - 1] > P[i] < P[i + 1]:
    IS_VALLEY[i] = 1

for i in range(N):
  PEAK_SUM[i + 1] = PEAK_SUM[i] + IS_PEAK[i]
  VALLEY_SUM[i + 1] = VALLEY_SUM[i] + IS_VALLEY[i]

for l in range(N):
  if l + 1 >= N or P[l] >= P[l + 1]:
    continue
  for r in range(l + 4, N + 1):
    PEAKS = PEAK_SUM[r - 1] - PEAK_SUM[l + 1]
    VALLEYS = VALLEY_SUM[r - 1] - VALLEY_SUM[l + 1]
    if PEAKS == 1 and VALLEYS == 1:
      ANSWER += 1

print(ANSWER)