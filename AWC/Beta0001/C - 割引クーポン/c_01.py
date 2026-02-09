N, K = map(int, input().split())
D_LIST = list(map(int, input().split()))

D_LIST.sort()

print(sum(D_LIST[:N - K]))