N = int(input())
D = list(map(int, input().split()))

sum = [0]
for d in D:
  sum.append(sum[-1] + d)

for i in range(N):
  for j in range(i+1, N):
    print(sum[j] - sum[i])