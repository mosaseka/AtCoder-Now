N, A, B = map(int, input().split())
S = str(input())

if A == 0 and B == 0:
  print(S)
elif A == 0:
  print(S[:-B])
elif B == 0:
  print(S[A:])
else:
  print(S[A:-B])