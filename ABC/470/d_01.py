N, Q = map(int, input().split())
P_LIST = list(map(int, input().split()))

P_LIST = [0] + P_LIST

P_REVERSE = [0] * (N + 1)
for i in range(1, N + 1):
  P_REVERSE[P_LIST[i]] = i

FLAG = False

for _ in range(Q):
  QUERY = list(map(int, input().split()))
  match QUERY[0]:
    case 1:
      x, y = QUERY[1], QUERY[2]

      if not FLAG:
        ALPHA, BETA = P_LIST[x], P_LIST[y]
        P_LIST[x], P_LIST[y] = BETA, ALPHA
        P_REVERSE[ALPHA], P_REVERSE[BETA] = y, x
      else:
        ALPHA, BETA = P_REVERSE[x], P_REVERSE[y]
        P_REVERSE[x], P_REVERSE[y] = BETA, ALPHA
        P_LIST[ALPHA], P_LIST[BETA] = y, x
    case 2:
      FLAG = not FLAG

if FLAG:
  print(*P_REVERSE[1:])
else:
  print(*P_LIST[1:])