N = int(input())

T_PAST, X_PAST, Y_PAST = 0, 0, 0

for i in range(N):
  T, X, Y = map(int, input().split())

  LENGTH = abs(X - X_PAST) + abs(Y - Y_PAST)
  TIME = T - T_PAST

  if LENGTH <= TIME and (LENGTH % 2) == (TIME % 2):
    pass
  else:
    print("No")
    exit()
  
  T_PAST, X_PAST, Y_PAST = T, X, Y

print("Yes")