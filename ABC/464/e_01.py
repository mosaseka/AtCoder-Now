from atcoder.segtree import SegTree

H, W, Q = map(int, input().split())

EVENTS = [[] for _ in range(H+1)]
LETTER = ["A"]

for i in range(1, Q+1):
  R, C , X = map(str, input().split())
  R, C = int(R), int(C)

  EVENTS[R].append((C, i))
  LETTER.append(X)

SEG = SegTree(max, 0, W)
ANSWER = [""] * H

for r in range(H, 0, -1):
  for c, index in EVENTS[r]:
    POSITION = W - c
    SEG.set(POSITION, max(SEG.get(POSITION), index))
  
  ROW = []
  for c in range(1, W+1):
    index = SEG.prod(0, W - c + 1)
    ROW.append(LETTER[index])
  
  ANSWER[r-1] = "".join(ROW)

print("\n".join(ANSWER))