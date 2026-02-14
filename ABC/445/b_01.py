N = int(input())
S_LIST = [str(input()) for _ in range(N)]
MAX_LEN = 0

for i in range(N):
  if len(S_LIST[i]) > MAX_LEN:
    MAX_LEN = len(S_LIST[i])

for i in range(N):
  CHECK = (MAX_LEN - len(S_LIST[i])) // 2
  print("." * CHECK + S_LIST[i] + "." * CHECK)