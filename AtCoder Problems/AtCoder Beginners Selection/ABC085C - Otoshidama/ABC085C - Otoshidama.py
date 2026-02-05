N, Y = map(int, input().split())

for i in range(N + 1):
  for j in range(N - i + 1):
    k = (Y - 10000*i - 5000*j) // 1000
    if k >= 0 and i + j + k == N:
      print(i, j, k)
      exit()

print(-1, -1, -1)