from bisect import bisect_left

N, K = map(int, input().split())
A_LIST = list(map(int, input().split()))

def CHECK(X):
  COUNT = 0

  for i, a in enumerate(A_LIST, 1):
    if a < X:
      COUNT += (X - a + i - 1) // i
      if COUNT > K:
        return False
  
  return True

LEFT = min(A_LIST)

RIGHT = float("inf")
for i, a in enumerate(A_LIST, 1):
    RIGHT = min(RIGHT, a + K * i)
RIGHT += 1


BISECT = bisect_left(
  range(LEFT, RIGHT),
  True,
  key=lambda x: not CHECK(x)
)

print(LEFT + BISECT - 1)