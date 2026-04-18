from collections import deque

T = int(input())

for _ in range(T):
  N, A, B = map(int, input().split())

  if N % 2 == 1 or (A + B) % 2 == 0:
    print("No")
    continue

  X = A - 1
  Y = B - 1
  TOP = 0
  BOTTOM = N - 1
  LEFT = 0
  RIGHT = N - 1
  HEAD = deque()
  TAIL = deque()

  while BOTTOM - TOP > 1:
    if TOP // 2 < X // 2:
      HEAD.append("R" * (N - 1))
      HEAD.append("D")
      HEAD.append("L" * (N - 1))
      HEAD.append("D")
      TOP += 2

    if X // 2 < BOTTOM // 2:
      TAIL.appendleft("R" * (N - 1))
      TAIL.appendleft("D")
      TAIL.appendleft("L" * (N - 1))
      TAIL.appendleft("D")
      BOTTOM -= 2

  while RIGHT - LEFT > 1:
    if LEFT // 2 < Y // 2:
      HEAD.append("DRUR")
      LEFT += 2

    if Y // 2 < RIGHT // 2:
      TAIL.appendleft("RURD")
      RIGHT -= 2

  if X == TOP:
    HEAD.append("DR")
  else:
    HEAD.append("RD")

  print("Yes")
  print("".join(HEAD) + "".join(TAIL))