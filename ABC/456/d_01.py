S = str(input())

DP = {"a": 0, "b": 0, "c": 0}
ANSWER = 0

for char in S:
  CHECK = (1 + ANSWER - DP[char]) % 998244353
  DP[char] = (DP[char] + CHECK) % 998244353

  ANSWER = (ANSWER + CHECK) % 998244353

print(ANSWER)