S, A, B, X = map(int, input().split())

CYCLE = A + B
COUNT = X // CYCLE
REMAIN = X % CYCLE

DIST = COUNT * A * S

REMAIN_RUN = min(REMAIN, A)
REMAIN_DIST = REMAIN_RUN * S

print(DIST + REMAIN_DIST)