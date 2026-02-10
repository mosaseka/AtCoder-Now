N = int(input())
SET = set()

for i in range(N):
  S = str(input())
  S_REVERSE = S[::-1]
  SET.add(min(S, S_REVERSE))

print(len(SET))