N, Q = map(int, input().split())

LOG = (Q+1).bit_length()
MASK = [(1 << i) - 1 for i in range(LOG)]
PAIR = [[0] * (1 << i) for i in range(LOG)]
RAW = [0] * N
EXPIRE = [[] for _ in range(Q+2)]
SHIFT = 0
ANSWER = 0
OUT = []

def flip(num):
  for i in range(LOG):
    PAIR[i][num & MASK[i]] ^= 1

for _ in range(Q):
  QUERY = list(map(int, input().split()))
  match QUERY[0]:
    case 1:
      x = QUERY[1] - 1

      if RAW[x] > SHIFT:
        NOW = RAW[x] - SHIFT
        ANSWER ^= NOW
        flip(RAW[x])
        RAW[x] += 1
        NOW += 1
        ANSWER ^= NOW
        flip(RAW[x])
      else:
        RAW[x] = SHIFT + 1
        ANSWER ^= 1
        flip(RAW[x])

      EXPIRE[RAW[x]].append(x)
    case 2:
      DELTA = 0
      for i in range(LOG):
        if PAIR[i][SHIFT & MASK[i]]:
          DELTA |= 1 << i

      ANSWER ^= DELTA
      SHIFT += 1

      for x in EXPIRE[SHIFT]:
        if RAW[x] == SHIFT:
          RAW[x] = 0
          flip(SHIFT)

  print(str(ANSWER))