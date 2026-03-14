from collections import defaultdict

N, L, R = map(int, input().split())
S = str(input())

ANSWER = 0
COUNT = defaultdict(int)

for j in range(N):
  ADD = j - L
  if 0 <= ADD:
    COUNT[S[ADD]] += 1

  REMOVE = j - R - 1
  if 0 <= REMOVE:
    COUNT[S[REMOVE]] -= 1
  
  ANSWER += COUNT[S[j]]

print(ANSWER)