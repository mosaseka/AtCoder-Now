import math

A, B, X = map(float, input().split())

PI = math.acos(-1.0)

X /= A

ANSWER = 0.0

if X > A*B / 2:
  ANSWER = math.atan2((A*B - X) * 2, A**2) * 180 / PI
else:
  ANSWER = math.atan2(B**2, X*2) * 180 / PI

print(ANSWER)