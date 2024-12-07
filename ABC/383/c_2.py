from collections import deque

def REACHABLE(H, W, D, S_LIST):
    VECTOR = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    REACHABLE_LIST = [[False] * W for _ in range(H)]
    QUEUE = deque()

    # 全てのスタート地点をキューに追加
    for i in range(H):
        for j in range(W):
            if S_LIST[i][j] == "H":
                QUEUE.append((i, j, 0))
                REACHABLE_LIST[i][j] = True

    while QUEUE:
        X, Y, DIST = QUEUE.popleft()
        if DIST >= D:
            continue
        for DX, DY in VECTOR:
            NX, NY = X + DX, Y + DY
            if 0 <= NX < H and 0 <= NY < W and not REACHABLE_LIST[NX][NY] and S_LIST[NX][NY] != "#":
                REACHABLE_LIST[NX][NY] = True
                QUEUE.append((NX, NY, DIST + 1))

    return REACHABLE_LIST

# 入力の読み込み
H, W, D = map(int, input().split())
S_LIST = [list(input()) for _ in range(H)]
REACHABLE_LIST = REACHABLE(H, W, D, S_LIST)
COUNT = 0

for i in range(H):
    for j in range(W):
        if REACHABLE_LIST[i][j]:
            COUNT += 1

print(COUNT)