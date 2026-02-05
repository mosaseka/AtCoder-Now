N, A, B = map(int, input().split())
ANSWER = 0

for i in range(1, N+1):
  SUM = 0
  CHECK = str(i)
  for j in range(len(CHECK)):
    SUM += int(CHECK[j])
  if A <= SUM <= B:
    ANSWER += i

print(ANSWER)