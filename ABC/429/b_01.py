N,M = map(int, input().split())
A_LIST = list(map(int, input().split()))

SUM = sum(A_LIST)

for i in range(N):
  if SUM - A_LIST[i] == M:
    print("Yes")
    exit()

print("No")