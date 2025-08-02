N, M = map(int, input().split())
A_LIST = list(map(int, input().split()))
B_LIST = list(map(int, input().split()))

for i in range(M):
  if B_LIST[i] in A_LIST:
    A_LIST.remove(B_LIST[i])

print(*A_LIST)