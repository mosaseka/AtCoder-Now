N, Q = map(int, input().split())
A_LIST = list(map(int, input().split()))
CHECK = A_LIST + A_LIST
PREF_SUM = 0

for i in range(2*N - 1, 0, -1):
  CHECK[i-1] += CHECK[i]

for i in range(Q):
  QUERY = list(map(int, input().split()))
  match QUERY[0]:
    case 1:
      C = QUERY[1]
      PREF_SUM += C
      PREF_SUM %= N
    case 2:
      L = QUERY[1] - 1
      R = QUERY[2]
      print(CHECK[PREF_SUM + L] - CHECK[PREF_SUM + R])
    case _:
      pass