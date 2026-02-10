N, P, Q = map(int, input().split())
D_LIST = list(map(int, input().split()))

minD = min(D_LIST)

print(min(Q + minD, P))