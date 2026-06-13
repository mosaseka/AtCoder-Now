from collections import deque
import sys
import time

input = sys.stdin.readline
START = time.perf_counter()

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
PATH_CACHE = {}
DELIVERY_CACHE = {}

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
  key = (position, goal)
  if key in PATH_CACHE:
    path = PATH_CACHE[key]
  else:
    path = BFS(position, goal)
    PATH_CACHE[key] = path
  ops, ndirection = MOVE(path, direction)
  return ops, goal, ndirection

def DELIVERY(position, direction, k):
  key = (position[0], position[1], direction, k)
  if key in DELIVERY_CACHE:
    return DELIVERY_CACHE[key]
  
  ops1, pos1, dir1 = ROUTE(position, direction, BALLS[k])
  ops2, pos2, dir2 = ROUTE(pos1, dir1, BASKETS[k])
  res = (ops1 + "S" + ops2 + "S", pos2, dir2)
  DELIVERY_CACHE[key] = res
  return res

def BETTER(a, b):
  if b is None:
    return True
  if a[0] != b[0]:
    return a[0] > b[0]
  return len(a[1]) < len(b[1])

def COMPLETE_GREEDY(position, direction, used, answer, order):
  while True:
    BEST = None

    for k in range(M):
      if used[k]:
        continue

      ops, pos2, dir2 = DELIVERY(position, direction, k)
      if len(answer) + len(ops) > T:
        continue

      if BEST is None or len(ops) < len(BEST[0]):
        BEST = (ops, pos2, dir2, k)

    if BEST is None:
      break

    ops, position, direction, idx = BEST
    answer.extend(ops)
    order.append(idx)
    used[idx] = True
  
  return len(order), answer[:T], order[:]

def SOLVE_BASE():
  POSITION = (0, 0)
  DIRECTION = 0
  USED = [False] * M
  ANSWER = []
  ORDER = []
  return COMPLETE_GREEDY(POSITION, DIRECTION, USED, ANSWER, ORDER)

def SOLVE_WITH_PREFIX(prefix):
  POSITION = (0, 0)
  DIRECTION = 0
  USED = [False] * M
  ANSWER = []
  ORDER = []
  
  for k in prefix:
    if USED[k]:
      continue
    ops, pos2, dir2 = DELIVERY(POSITION, DIRECTION, k)
    if len(ANSWER) + len(ops) > T:
      break
    ANSWER.extend(ops)
    ORDER.append(k)
    USED[k] = True
    POSITION = pos2
    DIRECTION = dir2
  
  return COMPLETE_GREEDY(POSITION, DIRECTION, USED, ANSWER, ORDER)

def SOLVE_BY_PRIORITY(priority):
  POSITION = (0, 0)
  DIRECTION = 0
  USED = [False] * M
  ANSWER = []
  ORDER = []
  
  for k in priority:
    if USED[k]:
      continue
    ops, pos2, dir2 = DELIVERY(POSITION, DIRECTION, k)
    if len(ANSWER) + len(ops) <= T:
      ANSWER.extend(ops)
      ORDER.append(k)
      USED[k] = True
      POSITION = pos2
      DIRECTION = dir2
  
  return COMPLETE_GREEDY(POSITION, DIRECTION, USED, ANSWER, ORDER)

def STATE_ESTIMATE(position, direction, used_bits):
  BEST = 10**9
  for k in range(M):
    if (used_bits >> k) & 1:
      continue
    ops, _, _ = DELIVERY(position, direction, k)
    if len(ops) < BEST:
      BEST = len(ops)
  if BEST == 10**9:
    return 0
  return BEST

def SOLVE_BEST_FIRST(base):
  DEADLINE = START + 1.35
  WIDTH = 90 if M <= 25 else 65
  EVAL_WIDTH = 14
  states = [(0, 0, (0, 0), 0, ())]
  BEST_SOL = base
  
  while states and time.perf_counter() < DEADLINE:
    candidates = []
    
    for length, used_bits, position, direction, order in states:
      if time.perf_counter() >= DEADLINE:
        break
      for k in range(M):
        if (used_bits >> k) & 1:
          continue
        ops, pos2, dir2 = DELIVERY(position, direction, k)
        new_length = length + len(ops)
        if new_length > T:
          continue
        new_bits = used_bits | (1 << k)
        estimate = STATE_ESTIMATE(pos2, dir2, new_bits)
        rank = new_length + estimate // 3
        candidates.append((rank, new_length, new_bits, pos2, dir2, order + (k,)))
    
    if not candidates:
      break
    
    candidates.sort(key=lambda x: (x[0], x[1], -x[2].bit_count()))
    states = []
    seen = set()
    
    for _, length, used_bits, position, direction, order in candidates:
      key = (used_bits, position, direction)
      if key in seen:
        continue
      seen.add(key)
      states.append((length, used_bits, position, direction, order))
      if len(states) >= WIDTH:
        break
    
    for state in states[:EVAL_WIDTH]:
      if time.perf_counter() >= DEADLINE:
        break
      sol = SOLVE_WITH_PREFIX(state[4])
      if BETTER(sol, BEST_SOL):
        BEST_SOL = sol
  
  return BEST_SOL

def SOLVE_HILL_CLIMB(base):
  DEADLINE = START + 1.65
  base_used = set(base[2])
  priority = base[2] + [k for k in range(M) if k not in base_used]
  current = SOLVE_BY_PRIORITY(priority)
  if BETTER(base, current):
    current = base
  
  improved = True
  while improved and time.perf_counter() < DEADLINE:
    improved = False
    
    for i in range(M):
      if time.perf_counter() >= DEADLINE:
        break
      for j in range(M):
        if i == j:
          continue
        cand_order = priority[:]
        x = cand_order.pop(i)
        cand_order.insert(j, x)
        cand = SOLVE_BY_PRIORITY(cand_order)
        if BETTER(cand, current):
          priority = cand_order
          current = cand
          improved = True
          break
      if improved:
        break
  
  return current

def EXPAND_MACRO(ops):
  LAST_MACRO = []
  RECORDING = False
  RECORDING_MACRO = []
  EXPANDED = []
  
  for op in ops:
    if op in "FRLS":
      EXPANDED.append(op)
      if RECORDING:
        RECORDING_MACRO.append(op)
    elif op == "M":
      if RECORDING:
        LAST_MACRO = RECORDING_MACRO
        RECORDING = False
      else:
        RECORDING_MACRO = []
        RECORDING = True
    elif op == "P":
      if LAST_MACRO:
        EXPANDED.extend(LAST_MACRO)
        if RECORDING:
          RECORDING_MACRO.extend(LAST_MACRO)
  
  return "".join(EXPANDED)

def BUILD_MACRO_OUTPUT(basic, macro, positions):
  L = len(macro)
  USE = set(positions)
  OUTPUT = []
  FIRST = True
  i = 0
  
  while i < len(basic):
    if i in USE:
      if FIRST:
        OUTPUT.append("M")
        OUTPUT.extend(macro)
        OUTPUT.append("M")
        FIRST = False
      else:
        OUTPUT.append("P")
      i += L
    else:
      OUTPUT.append(basic[i])
      i += 1
  
  return OUTPUT

def COMPRESS_MACRO(answer):
  basic = "".join(answer)
  n = len(basic)
  if n < 4:
    return answer
  
  BEST_SCORE = (0, 0, 0, 0)
  BEST_MACRO = None
  BEST_POSITIONS = None
  DEADLINE = time.perf_counter() + 0.25
  MAX_LEN = min(80, n)
  
  for L in range(2, MAX_LEN + 1):
    EXPIRED = False
    POSITIONS = {}
    LIMIT = n - L + 1
    
    for i in range(LIMIT):
      if (i & 2047) == 0 and time.perf_counter() > DEADLINE:
        EXPIRED = True
        break
      macro = basic[i:i+L]
      if macro in POSITIONS:
        POSITIONS[macro].append(i)
      else:
        POSITIONS[macro] = [i]
    
    for idx, (macro, pos_list) in enumerate(POSITIONS.items()):
      if (idx & 4095) == 0 and time.perf_counter() > DEADLINE:
        EXPIRED = True
        break
      if len(pos_list) < 2:
        continue
      
      selected = []
      last = -L
      for pos in pos_list:
        if last + L <= pos:
          selected.append(pos)
          last = pos
      
      count = len(selected)
      if count < 2:
        continue
      
      gain = (count - 1) * (L - 1) - 2
      if gain <= 0:
        continue
      
      score = (
        gain,
        1 if "S" in macro else 0,
        1 if ("L" in macro or "R" in macro) else 0,
        L,
      )
      if BEST_SCORE < score:
        BEST_SCORE = score
        BEST_MACRO = macro
        BEST_POSITIONS = selected
    
    if EXPIRED:
      break
  
  if BEST_MACRO is None:
    return answer
  
  output = BUILD_MACRO_OUTPUT(basic, BEST_MACRO, BEST_POSITIONS)
  if len(output) < n and EXPAND_MACRO(output) == basic:
    return output
  
  return answer

BEST = SOLVE_BASE()

CAND = SOLVE_BEST_FIRST(BEST)
if BETTER(CAND, BEST):
  BEST = CAND

CAND = SOLVE_HILL_CLIMB(BEST)
if BETTER(CAND, BEST):
  BEST = CAND

ANSWER = BEST[1]
if BEST[0] == M:
  ANSWER = COMPRESS_MACRO(ANSWER)

if ANSWER:
  print("\n".join(ANSWER))
