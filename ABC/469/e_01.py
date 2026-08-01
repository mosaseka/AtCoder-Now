from bisect import bisect_left

N, K = map(int, input().split())
S = str(input())

POSITION = []

for i, c in enumerate(S):
  if c == "o":
    POSITION.append(i)

def CHECK(RATE):
  BEST = float("inf")
  
  for j, pj in enumerate(POSITION):
    i = j - K + 1

    if i >= 0:
      BEST = min(BEST, i - RATE * POSITION[i])
      if (j+1) - RATE * (pj+1) >= BEST:
        return True
  
  return False

BORDER = 10**12

INDEX = bisect_left(
  range(BORDER+1),
  True,
  key = lambda x: not CHECK(x / BORDER)
)

ANSWER = (INDEX-1) / BORDER
print(ANSWER)