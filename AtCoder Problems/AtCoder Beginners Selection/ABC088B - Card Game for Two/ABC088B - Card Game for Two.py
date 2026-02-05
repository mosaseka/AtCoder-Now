N = int(input())
A_LIST = list(map(int, input().split()))
alice = 0
bob = 0

A_LIST.sort(reverse=True)

for i in range(N):
  if i % 2 == 0:
    alice += A_LIST[i]
  else:
    bob += A_LIST[i]

print(alice - bob)