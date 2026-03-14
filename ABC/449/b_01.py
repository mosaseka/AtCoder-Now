H, W, Q = map(int, input().split())

for _ in range(Q):
  QUERY = list(map(int, input().split()))

  match QUERY[0]:
    case 1:
      R = QUERY[1]
      print(W * R)
      H -= R
    case 2:
      C = QUERY[1]
      print(H * C)
      W -= C