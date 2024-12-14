N, D = map(int, input().split())
S = str(input())
ANSWER = 0

S = S.replace("@", ".", D)

ANSWER = S.count(".")
print(ANSWER)