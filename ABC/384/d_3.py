N, S = map(int,input().split())
A_LIST = list(map(int,input().split()))
SUM_A = sum(A_LIST)
NOW = 0
START = 0

S %= SUM_A

for i in range(2 * N):
  NOW += A_LIST[i % N]
    
  while NOW > S and START <= i:
    NOW -= A_LIST[START % N]
    START += 1

  if NOW == S:
    print("Yes")
    exit()

print("No")