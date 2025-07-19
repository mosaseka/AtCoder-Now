T = int(input())

for i in range(T):
  N = int(input())
  S = str(input())
  DP = [False] * (2**N)

  DP[0] = True
  
  for j in range(2**N):
    if not DP[j]:
      continue
    for k in range(N):
      if j & (1 << k):
        continue  
      NEW = j | (1 << k)
      if NEW > 0 and S[NEW - 1] == "0":
        DP[NEW] = True
  if DP[2**N - 1]:
    print("Yes")
  else:
    print("No")