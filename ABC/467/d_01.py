T = int(input())

for _ in range(T):
  Px, Py, Qx, Qy, Rx, Ry, Sx, Sy = map(int, input().split())

  if (Qx-Px)*(Sy-Ry) - (Qy-Py)*(Sx-Rx) != 0:
    print("Yes")
  else:
    if (Sx-Rx) * (Px+Qx-Rx-Sx) + (Sy-Ry)*(Py+Qy-Ry-Sy) == 0:
      print("Yes")
    else:
      print("No")