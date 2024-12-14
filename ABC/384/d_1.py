N,S = map(int,input().split())
A_LIST = list(map(int,input().split()))
SUM_A = sum(A_LIST)
CHECK = [A_LIST[i:j] for i in range(N) for j in range(i+1, N+1)]
#print(CHECK)

S %= SUM_A
#print(S)

for i in range(len(CHECK)):
  if S - sum(CHECK[i]) == 0:
    print("Yes")
    exit()

print("No")