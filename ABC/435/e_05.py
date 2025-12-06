from sortedcontainers import SortedList

N, Q = map(int, input().split())
WHITE = SortedList()
WHITE.add((N, 1))
WHITE_TOTAL = N

for i in range(Q):
  L, R = map(int, input().split())
  INDEX = WHITE.bisect_left((L, -1))
  TO_ADD = []
  while INDEX < len(WHITE):
    SR, SL = WHITE[INDEX]
    if R < SL:
      break
    if SL < L and R < SR:
      TO_ADD.append((L - 1, SL))
      TO_ADD.append((SR, R + 1))
    elif SL < L and L <= SR:
      TO_ADD.append((L - 1, SL))
    elif R < SR and SL <= R:
      TO_ADD.append((SR, R + 1))
    WHITE_TOTAL -= min(SR, R) - max(SL, L) + 1
    del WHITE[INDEX]
  for INTERVAL in TO_ADD:
    WHITE.add(INTERVAL)
  print(WHITE_TOTAL)