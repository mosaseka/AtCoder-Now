N = int(input())
P = list(map(int, input().split()))
ANSWER = 0

for i in range(N - 4):
  if P[i] >= P[i + 1]:
    continue
  PEAKS = 0
  VALLEYS = 0
  for j in range(i + 1, i + 4):
    if P[j - 1] < P[j] > P[j + 1]:
      PEAKS += 1
    elif P[j - 1] > P[j] < P[j + 1]:
      VALLEYS += 1
  if PEAKS == 1 and VALLEYS == 1:
    ANSWER += 1

print(ANSWER*2)