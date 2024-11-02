N = int(input())
A_LIST = list(map(int, input().split()))
B_LIST = []
CHECK = {}

for i in range(N):
    B_LIST.append(CHECK.get(A_LIST[i], -1))
    CHECK[A_LIST[i]] = i + 1

print(*B_LIST)
