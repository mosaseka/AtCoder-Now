N, M = map(int, input().split())
C_LIST = list(map(int, input().split()))
R_LIST = list(map(int, input().split()))

ANSWER = 0
INDEX = 0

C_LIST.sort()
R_LIST.sort()

for c in C_LIST:
  while INDEX < M and R_LIST[INDEX] < c:
    INDEX += 1
  if INDEX < M:
    ANSWER += 1
    INDEX += 1

print(ANSWER)