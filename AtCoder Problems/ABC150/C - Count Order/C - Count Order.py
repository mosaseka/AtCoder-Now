from itertools import permutations

N = int(input())
P_TUPLE = tuple(map(int, input().split()))
Q_TUPLE = tuple(map(int, input().split()))

NUM = [i+1 for i in range(N)]
PERM = []
A = 0
B = 0

for i in permutations(NUM, N):
  PERM.append(i)

A = PERM.index(P_TUPLE)
B = PERM.index(Q_TUPLE)

print(abs(A-B))