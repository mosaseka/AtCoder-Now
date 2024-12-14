N,D = map(int,input().split())
S = list(map(str,input()))
COUNT = 0

S.reverse()

for i in range(N):
  if COUNT == D:
    S.reverse()
    print("".join(S))
    exit()
  else:
    if S[i] == "@":
      COUNT += 1
      S[i] = "."

S.reverse()
print("".join(S))