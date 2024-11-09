N, K = map(int,input().split())
S = list(map(str,input()))
COUNT = 0

for i in range(N - K + 1):
  if ''.join(S[i:i+K]) == "O" * K:
    COUNT += 1
    S[i:i+K] = ['X'] * K

print(COUNT)