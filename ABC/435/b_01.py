N = int(input())
A_LIST = list(map(int, input().split()))
ANSWER = 0
FLAG = True

for l in range(N):
  for r in range(l, N):
    SUM = sum(A_LIST[l:r+1])
    FLAG = True
    for i in range(l, r+1):
      if SUM % A_LIST[i] == 0:
        FLAG = False
        break
    if FLAG:
      ANSWER += 1

print(ANSWER)