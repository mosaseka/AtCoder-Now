N, K = map(int, input().split())
LR_LIST = [tuple(map(int, input().split())) for _ in range(N)]

LR_LIST.sort(key=lambda x: x[1])

def CHECK(DIST):
  COUNT = 0
  LAST_RIGHT = -10**18

  for left, right in LR_LIST:
    if left - LAST_RIGHT >= DIST:
      COUNT += 1
      LAST_RIGHT = right

      if COUNT >= K:
        return True
    
  return False

if not CHECK(1):
  print(-1)
  exit()

left = 1
right = 10**9 + 1

while right - left > 1:
  middle = (left + right) // 2

  if CHECK(middle):
    left = middle
  else:
    right = middle

print(left)