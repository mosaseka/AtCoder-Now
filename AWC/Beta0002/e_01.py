from collections import defaultdict

def enumSum(LIST):
  SUMS = defaultdict(int)
  N = len(LIST)
  for i in range(1 << N):
    SUM = 0
    for j in range(N):
      if i & (1 << j):
        SUM += LIST[j]
    SUMS[SUM] += 1
  return SUMS

N, S = map(int, input().split())
A_LIST = list(map(int, input().split()))

MID = N // 2
BEFORE = A_LIST[:MID]
AFTER = A_LIST[MID:]

SUMS_BEFORE = enumSum(BEFORE)
SUMS_AFTER = enumSum(AFTER)

ANSWER = 0

for alpha, beta in SUMS_BEFORE.items():
  if alpha <= S:
    beta = S - alpha
    if beta in SUMS_AFTER:
      ANSWER += SUMS_BEFORE[alpha] * SUMS_AFTER[beta]

print(ANSWER)