N = int(input())
T_LIST = list(map(int, input().split()))
ANSWER = []

for i in range(N):
  T_LIST[i] = [T_LIST[i], i + 1]

T_LIST.sort()

for i in range(3):
  ANSWER.append(T_LIST[i][1])

print(*ANSWER)