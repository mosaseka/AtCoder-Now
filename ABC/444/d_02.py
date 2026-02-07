N = int(input())
A_LIST = list(map(int, input().split()))

A = sorted(A_LIST)

ANSWER = []
CARRY = 0
POS = 0
INDEX = 0
MAX_POS = A[-1]

while POS < MAX_POS or CARRY > 0:
  while INDEX < N and A[INDEX] <= POS:
    INDEX += 1
  count = N - INDEX

  if count == 0:
    ANSWER.append(CARRY % 10)
    CARRY //= 10
    POS += 1
    continue

  NEXT = A[INDEX] if INDEX < N else MAX_POS
  REMAINING = NEXT - POS

  VAL = count + CARRY
  d = VAL % 10
  NEW_CARRY = VAL // 10

  if NEW_CARRY == CARRY:
    ANSWER.extend([d] * REMAINING)
    CARRY = NEW_CARRY
    POS = NEXT
  else:
    ANSWER.append(d)
    CARRY = NEW_CARRY
    POS += 1

ANSWER.reverse()
print(''.join(map(str, ANSWER)))