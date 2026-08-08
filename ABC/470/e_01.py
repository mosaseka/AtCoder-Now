N, L = map(int, input().split())
A_LIST = list(map(int, input().split()))

PREV = [[0.0] * (N+3) for _ in range(N+3)]

for life in range(1, L+1):
  NOW = [[0.0] * (N+3) for _ in range(N+3)]

  for total in range(1, N+1):
    for u in range(total + 1):
      k = total - u
      HIDDEN = 2 * u + k
      NUM = 0.0

      if k > 0:
        NUM += k / HIDDEN * (1.0 + NOW[u][k-1])

      if u > 0:
        DEN = HIDDEN - 1

        NEXT = 1.0 / DEN * (1.0 + NOW[u-1][k])

        if life > 1:
          if k > 0:
            NEXT += k / DEN * (1.0 + PREV[u-1][k])
          if u >= 2:
            NEXT += 2.0 * (u - 1) / DEN * PREV[u-2][k+2]

        NUM += 2.0 * u / HIDDEN * NEXT

      NOW[u][k] = NUM

  PREV = NOW

EXPECT = PREV[N][0]

ANSWER = EXPECT * sum(A_LIST) / N
print(ANSWER)