N, M = map(int, input().split())
X_LIST = list(map(int, input().split()))

X_LIST.sort()

D = [X_LIST[i + 1] - X_LIST[i] for i in range(N - 1)]

D.sort()

ANS = sum(D[:N - M]) if N > M else 0

print(ANS)