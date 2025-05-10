from itertools import combinations

N = int(input())
A = list(map(int, input().split()))
ANSWER = 0

for i in combinations(A, 2):
  ANSWER += i[0] * i[1]

print(ANSWER)