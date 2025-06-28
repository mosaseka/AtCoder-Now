N = int(input())
COUNT = 0

for i in range(N):
  CHECK = list(map(int, input().split()))
  if CHECK[0] < CHECK[1]:
    COUNT += 1

print(COUNT)