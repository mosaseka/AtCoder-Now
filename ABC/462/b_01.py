N = int(input())
A_LIST = []
GIFT = [set() for _ in range(N)]

for i in range(N):
  INPUT = list(map(int, input().split()))
  K = INPUT[0]
  A_LIST = INPUT[1:]

  for a in A_LIST:
    GIFT[a-1].add(i+1)

for i in range(N):
  print(len(GIFT[i]), *sorted(GIFT[i]))