from collections import deque
import time

N, M, T = map(int, input().split())
V = [input().strip() for _ in range(N)]
H = [input().strip() for _ in range(N-1)]

BALLS = []
BASKETS = []
for i in range(M):
  B, C, D, E = map(int, input().split())
  BALLS.append((B, C))
  BASKETS.append((D, E))

DI = [0, 1, 0, -1]
DJ = [1, 0, -1, 0]

def CAN(i, j, nd):
  match nd:
    case 0:
      return j+1 < N and V[i][j] == "0"
    case 1:
      return i+1 < N and H[i][j] == "0"
    case 2:
      return j-1 >= 0 and V[i][j-1] == "0"
    case _:
      return i-1 >= 0 and H[i-1][j] == "0"

def BFS(start, goal):
  if start == goal:
    return []
  
  NOW = [[None] * N for _ in range(N)]
  DEQ = deque([start])
  NOW[start[0]][start[1]] = (-1, -1, -1)

  while DEQ:
    i, j = DEQ.popleft()
    for nd in range(4):
      if not CAN(i, j, nd):
        continue
      ni, nj = i + DI[nd], j + DJ[nd]
      if NOW[ni][nj] is not None:
        continue
      NOW[ni][nj] = (i, j, nd)
      if (ni, nj) == goal:
        DEQ.clear()
        break
      DEQ.append((ni, nj))
  
  PATH = []
  ci, cj = goal
  while (ci, cj) != start:
    pi, pj, nd = NOW[ci][cj]
    PATH.append(nd)
    ci, cj = pi, pj
  
  PATH.reverse()
  return PATH

def TURN(now, next):
  DIFF = (next - now) % 4
  match DIFF:
    case 0:
      return ""
    case 1:
      return "R"
    case 2:
      return "RR"
    case _:
      return "L"

def MOVE(path, now):
  LIST = []
  d = now
  for nd in path:
    LIST.append(TURN(d, nd))
    LIST.append("F")
    d = nd
  return "".join(LIST), d

def ROUTE(position, direction, goal):
  path = BFS(position, goal)
  ops, ndirection = MOVE(path, direction)
  return ops, goal, ndirection

def EXPAND_COMMANDS(commands):
  last_macro = []
  recording = []
  is_recording = False
  expanded = []
  
  for ch in commands:
    if ch == "M":
      if is_recording:
        last_macro = recording
        recording = []
        is_recording = False
      else:
        recording = []
        is_recording = True
    elif ch == "P":
      expanded.extend(last_macro)
      if is_recording:
        recording.extend(last_macro)
    else:
      expanded.append(ch)
      if is_recording:
        recording.append(ch)
  
  return "".join(expanded)

def ADD_CANDIDATE(candidates, start, candidate):
  LIMIT = 8
  arr = candidates[start]
  if len(arr) < LIMIT:
    arr.append(candidate)
    return
  
  worst_idx = 0
  worst_key = (arr[0][1], -arr[0][0])
  for i in range(1, len(arr)):
    key = (arr[i][1], -arr[i][0])
    if key < worst_key:
      worst_key = key
      worst_idx = i
  
  new_key = (candidate[1], -candidate[0])
  if worst_key < new_key:
    arr[worst_idx] = candidate

def BUILD_MACRO_OUTPUT(basic, candidate):
  end, gain, macro, positions = candidate
  length = len(macro)
  res = ["M"]
  res.extend(macro)
  res.append("M")
  
  prev = positions[0] + length
  for p in positions[1:]:
    if prev < p:
      res.extend(basic[prev:p])
    res.append("P")
    prev = p + length
  
  return res

def COMPRESS_MACRO_DP(answer):
  basic = "".join(answer)
  n = len(basic)
  if n < 4:
    return answer
  
  MIN_LEN = 2
  MAX_LEN = min(200, n // 2)
  MAX_CHAIN = 30
  START_TIME = time.perf_counter()
  TIME_LIMIT = 1.5
  CANDIDATES = [[] for _ in range(n)]
  
  for length in range(MIN_LEN, MAX_LEN + 1):
    if TIME_LIMIT < time.perf_counter() - START_TIME:
      break
    
    POS = {}
    for i in range(n - length + 1):
      sub = basic[i:i+length]
      if sub not in POS:
        POS[sub] = []
      POS[sub].append(i)
    
    for macro, positions in POS.items():
      if len(positions) < 2:
        continue
      
      m = len(positions)
      next_idx = [m] * m
      r = 1
      for i, p in enumerate(positions):
        if r < i + 1:
          r = i + 1
        while r < m and positions[r] < p + length:
          r += 1
        next_idx[i] = r
      
      for i, p in enumerate(positions):
        used = [p]
        idx = i
        for cnt in range(2, MAX_CHAIN + 1):
          idx = next_idx[idx]
          if idx >= m:
            break
          used.append(positions[idx])
          
          gain = (cnt - 1) * (length - 1) - 2
          if gain <= 0:
            continue
          
          end = used[-1] + length
          ADD_CANDIDATE(CANDIDATES, p, (end, gain, macro, tuple(used)))
  
  dp = [0] * (n + 1)
  choice = [None] * n
  
  for i in range(n - 1, -1, -1):
    best = dp[i + 1]
    best_cand = None
    for cand in CANDIDATES[i]:
      end, gain, macro, positions = cand
      value = gain + dp[end]
      if best < value:
        best = value
        best_cand = cand
    
    dp[i] = best
    choice[i] = best_cand
  
  if dp[0] <= 0:
    return answer
  
  result = []
  i = 0
  while i < n:
    cand = choice[i]
    if cand is None:
      result.append(basic[i])
      i += 1
    else:
      result.extend(BUILD_MACRO_OUTPUT(basic, cand))
      i = cand[0]
  
  if len(result) < n and EXPAND_COMMANDS(result) == basic:
    return result
  return answer

POSITION = (0, 0)
DIRECTION = 0
USED = [False] * M
ANSWER = []

while True:
  BEST = None

  for k in range(M):
    if USED[k]:
      continue

    ops1, pos1, dir1 = ROUTE(POSITION, DIRECTION, BALLS[k])
    ops2, pos2, dir2 = ROUTE(pos1, dir1, BASKETS[k])
    ops = ops1 + "S" + ops2 + "S"

    if len(ANSWER) + len(ops) > T:
      continue

    if BEST is None or len(ops) < len(BEST[0]):
      BEST = (ops, pos2, dir2, k)
    
  
  if BEST is None:
    break

  ops, POSITION, DIRECTION, idx = BEST
  ANSWER.extend(ops)
  USED[idx] = True

ANSWER = ANSWER[:T]
ANSWER = COMPRESS_MACRO_DP(ANSWER)

if ANSWER:
  print("\n".join(ANSWER))