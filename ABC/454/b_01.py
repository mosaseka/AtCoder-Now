N, M = map(int, input().split())
F_LIST = list(map(int, input().split()))

if len(set(F_LIST)) == N:
  print("Yes")
else:
  print("No")

CHECK = set()

for i in range(N):
  CHECK.add(F_LIST[i])

if len(CHECK) == M:
  print("Yes")
else:
  print("No")