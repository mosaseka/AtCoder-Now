N = int(input())
A_LIST = list(map(int, input().split()))
ANSWER = 0

for i in range(N):
  if (i+1) % 2 == 0:
    pass
  else:
    ANSWER += A_LIST[i]

print(ANSWER)