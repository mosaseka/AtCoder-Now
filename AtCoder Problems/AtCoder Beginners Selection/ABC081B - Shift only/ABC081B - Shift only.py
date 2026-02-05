N = int(input())
A_LIST = list(map(int, input().split()))

FLAG = False
ANSWER = 0

while True:
  for i in range(N):
    if A_LIST[i] % 2 != 0:
      FLAG = True
      break
  if FLAG:
    break
  for i in range(N):
    A_LIST[i] //= 2
  ANSWER += 1

print(ANSWER)