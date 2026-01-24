Q = int(input())
VOLUME = 0
PLAY = False

for i in range(Q):
  A = int(input())
  match A:
    case 1:
      VOLUME += 1
    case 2:
      VOLUME -= 1
      VOLUME = max(0, VOLUME)
    case 3:
      PLAY = not PLAY
    case _:
      pass

  if PLAY and VOLUME >= 3:
    print("Yes")
  else:
    print("No")