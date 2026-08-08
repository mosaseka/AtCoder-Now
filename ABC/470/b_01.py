from collections import Counter

N = int(input())
C_LIST = list(map(int, input().split()))

C_COUNT = Counter(C_LIST)
ANSWER = N - max(C_COUNT.values())

print(ANSWER)