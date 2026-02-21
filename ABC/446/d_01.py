from bisect import bisect_left

N = int(input())
A_LIST = list(map(int, input().split()))

CHECK = [A_LIST[0]]

for i in range(N):
  if A_LIST[i] > CHECK[-1]:
    CHECK.append(A_LIST[i])
  else:
    INDEX = bisect_left(CHECK, A_LIST[i])
    CHECK[INDEX] = A_LIST[i]

print(len(CHECK))