S = str(input())

NUM = set(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])

ANSWER = ""

for char in S:
  if char in NUM:
    ANSWER += char

print(ANSWER)