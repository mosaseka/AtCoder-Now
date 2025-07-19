N, M = map(int, input().split())
EXCHANGES = []

for i in range(M):
  A, B = map(int, input().split())
  EXCHANGES.append([A, B, B - A])

EXCHANGES.sort(key=lambda x: x[2], reverse=True)

TOTAL_STICKERS = 0
CURRENT_BOTTLES = N

for i in range(M):
  A, B, LOSS = EXCHANGES[i]
  if CURRENT_BOTTLES >= A:
    if LOSS < 0:
      MAX_EXCHANGES = (CURRENT_BOTTLES - A) // (-LOSS) + 1
      TOTAL_STICKERS += MAX_EXCHANGES
      CURRENT_BOTTLES += MAX_EXCHANGES * LOSS
    elif LOSS == 0:
      pass

print(TOTAL_STICKERS)