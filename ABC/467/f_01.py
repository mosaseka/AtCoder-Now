from atcoder.segtree import SegTree

N, Q = map(int, input().split())
A_LIST = list(map(int, input().split()))
B_LIST = list(map(int, input().split()))

QUERIES = []
COORDS = B_LIST.copy()

for _ in range(Q):
  T, I, X = map(int, input().split())
  I -= 1
  QUERIES.append((T, I, X))
  if T == 2:
    COORDS.append(X)

COORDS = sorted(set(COORDS))
INDEX = {v: i for i, v in enumerate(COORDS)}
LEN = len(COORDS)

A_SUM = [0] * LEN
for a, b in zip(A_LIST, B_LIST):
  A_SUM[INDEX[b]] += a

def make_node(num):
  if A_SUM[num] == 0:
    return(0, -float("inf"))
  else:
    return(A_SUM[num], COORDS[num] + A_SUM[num])

def op(left, right):
  TOTAL = left[0] + right[0]
  MAX = max(right[1], right[0] + left[1])
  return(TOTAL, MAX)

SEG = SegTree(op, (0, -float("inf")), [make_node(i) for i in range(LEN)])
ANSWER = 0

for t, i, x in QUERIES:
  match t:
    case 1:
      NUM = INDEX[B_LIST[i]]
      A_SUM[NUM] += x - A_LIST[i]
      A_LIST[i] = x
      SEG.set(NUM, make_node(NUM))
    case 2:
      OLD = INDEX[B_LIST[i]]
      NEW = INDEX[x]
      A = A_LIST[i]

      if OLD != NEW:
        A_SUM[OLD] -= A
        SEG.set(OLD, make_node(OLD))
        A_SUM[NEW] += A
        SEG.set(NEW, make_node(NEW))
        B_LIST[i] = x
    
  print(str(SEG.all_prod()[1]))
