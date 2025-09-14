from collections import deque
import heapq

N, K = map(int, input().split())
QUEUE = deque()
EXIT_HEAP = []
NOW = 0
ENTER_TIMES = [-1] * N
TIME = 0
GROUP_INDEX = 0
INFTY = 10**19
GROUPS = []
PEOPLE = 0

for i in range(N):
  A, B, C = map(int, input().split())
  GROUPS.append((A, B, C, i))

GROUPS.sort()

while GROUP_INDEX < N or QUEUE or EXIT_HEAP:
  while EXIT_HEAP and EXIT_HEAP[0][0] <= TIME:
    EXIT_TIME, PEOPLE = heapq.heappop(EXIT_HEAP)
    NOW -= PEOPLE

  while GROUP_INDEX < N and GROUPS[GROUP_INDEX][0] <= TIME:
    QUEUE.append(GROUPS[GROUP_INDEX])
    GROUP_INDEX += 1

  FLAG = False
  while QUEUE and NOW + QUEUE[0][2] <= K:
    A, B, C, INDEX = QUEUE.popleft()
    ENTER_TIMES[INDEX] = TIME
    NOW += C
    heapq.heappush(EXIT_HEAP, (TIME + B, C))
    FLAG = True

  if FLAG:
    continue

  if QUEUE:
    NEXT_EXIT = EXIT_HEAP[0][0] if EXIT_HEAP else INFTY
    TIME = NEXT_EXIT
    continue

  NEXT_ARRIVAL = GROUPS[GROUP_INDEX][0] if GROUP_INDEX < N else INFTY
  NEXT_EXIT = EXIT_HEAP[0][0] if EXIT_HEAP else INFTY
  NEXT_TIME = min(NEXT_ARRIVAL, NEXT_EXIT)

  if NEXT_TIME == INFTY:
    break
  TIME = max(TIME, NEXT_TIME)

for i in range(N):
  print(ENTER_TIMES[i])