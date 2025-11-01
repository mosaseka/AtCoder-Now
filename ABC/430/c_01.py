import bisect

N, A, B = map(int, input().split())
S = str(input())
A_COUNT = [0] * (N + 1)
B_COUNT = [0] * (N + 1)
ANSWER = 0

for i in range(N):
  if S[i] == "a":
    A_COUNT[i+1] = A_COUNT[i] + 1
    B_COUNT[i+1] = B_COUNT[i]
  else:
    A_COUNT[i+1] = A_COUNT[i]
    B_COUNT[i+1] = B_COUNT[i] + 1

for l in range(1, N + 1):
  A_TARGET = A_COUNT[l - 1] + A
  B_TARGET = B_COUNT[l - 1] + B
  MIN = bisect.bisect_left(A_COUNT, A_TARGET, l, N + 1)
  if MIN <= N and A_COUNT[MIN] < A_TARGET:
    MIN += 1
  MAX = bisect.bisect_left(B_COUNT, B_TARGET, l, N + 1) - 1
  if MIN <= MAX and MIN <= N:
    ANSWER += MAX - MIN + 1

print(ANSWER)