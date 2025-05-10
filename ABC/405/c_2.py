N = int(input())
A = list(map(int, input().split()))

SUM = sum(A)
SQR = sum(a * a for a in A)

ANSWER = (SUM * SUM - SQR) // 2
print(ANSWER)