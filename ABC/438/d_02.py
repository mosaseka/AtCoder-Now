N = int(input())
A_LIST = list(map(int, input().split()))
B_LIST = list(map(int, input().split()))
C_LIST = list(map(int, input().split()))
A_SUM = [0] * (N + 1)
B_SUM = [0] * (N + 1)
C_SUM = [0] * (N + 1)
ANSWER = float("-inf")
X_MAX = float("-inf")

for i in range(N):
  A_SUM[i + 1] = A_SUM[i] + A_LIST[i]
  B_SUM[i + 1] = B_SUM[i] + B_LIST[i]
  C_SUM[i + 1] = C_SUM[i] + C_LIST[i]

for y in range(2, N):
  x = y - 1
  X_MAX = max(X_MAX, (A_SUM[x] - B_SUM[x]))
  TOTAL = X_MAX + (B_SUM[y] - C_SUM[y]) + C_SUM[N]
  ANSWER = max(ANSWER, TOTAL)

print(ANSWER)