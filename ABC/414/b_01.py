N = int(input())
COUNT = 0
ANSWER = ""

for i in range(N):
  C, L = map(str, input().split())
  L = int(L)
  COUNT += L
  if COUNT > 100:
    print("Too Long")
    exit()
  ANSWER += C * L

print(ANSWER)