from bisect import bisect_right

def build_positions(STRING):
  POSITIONS = [[] for _ in range(26)]
  for i, CH in enumerate(STRING, 1):
    POSITIONS[ord(CH) - 97].append(i)
  return POSITIONS

def count_prefix(N, CHAR_ID):
  if N <= 0:
    return 0

  INDEX = TARGET
  ANSWER = 0

  while INDEX >= 3:
    LEFT_LENGTH = LENGTHS[INDEX - 1]
    if N <= LEFT_LENGTH:
      INDEX -= 1
    else:
      ANSWER += TOTALS[INDEX - 1][CHAR_ID]
      N -= LEFT_LENGTH
      INDEX -= 2

  if INDEX == 1:
    ANSWER += bisect_right(X_POSITIONS[CHAR_ID], N)
  else:
    ANSWER += bisect_right(Y_POSITIONS[CHAR_ID], N)

  return ANSWER

X = str(input())
Y = str(input())
Q = int(input())

X_POSITIONS = build_positions(X)
Y_POSITIONS = build_positions(Y)

LENGTHS = [0, len(X), len(Y)]
TOTALS = [
  None,
  [len(POS) for POS in X_POSITIONS],
  [len(POS) for POS in Y_POSITIONS],
]

TARGET = 2
while LENGTHS[TARGET] < 10 ** 18:
  LENGTHS.append(LENGTHS[-1] + LENGTHS[-2])
  TOTALS.append([TOTALS[-1][i] + TOTALS[-2][i] for i in range(26)])
  TARGET += 1

for _ in range(Q):
  QUERY = list(map(str, input().split()))
  L = int(QUERY[0])
  R = int(QUERY[1])
  CHAR_ID = ord(QUERY[2]) - 97
  print(count_prefix(R, CHAR_ID) - count_prefix(L - 1, CHAR_ID))