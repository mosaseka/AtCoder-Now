L, R, D, U = map(int, input().split())

XS = []
if L <= -1:
  NR = min(R, -1)
  XS.append((-NR, -L))
if L <= 0 <= R:
  XS.append((0, 0))
if R >= 1:
  PL = max(L, 1)
  XS.append((PL, R))

YS = []
if D <= -1:
  NR = min(U, -1)
  YS.append((-NR, -D))
if D <= 0 <= U:
  YS.append((0, 0))
if U >= 1:
  PL = max(D, 1)
  YS.append((PL, U))

ANSWER = 0

for x1, x2 in XS:
  for y1, y2 in YS:
    SUB = 0

    for px, py, sgn in [
      (x2, y2, 1),
      (x1 - 1, y2, -1),
      (x2, y1 - 1, -1),
      (x1 - 1, y1 - 1, 1),
    ]:
      if px < 0 or py < 0:
        SUM = 0
      else:
        M = min(px, py)
        T = M // 2
        SUM = (T + 1) * (2 * T + 1)

        if px > M:
          A = M + 1
          B = px
          EVEN_COUNT = B // 2 - (A - 1) // 2
          SUM += (py + 1) * EVEN_COUNT
        elif py > M:
          A = M + 1
          B = py
          EVEN_COUNT = B // 2 - (A - 1) // 2
          SUM += (px + 1) * EVEN_COUNT

      SUB += sgn * SUM

    ANSWER += SUB

print(ANSWER)