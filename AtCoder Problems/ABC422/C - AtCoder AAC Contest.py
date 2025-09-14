from math import floor

T = int(input())

for i in range(T):
  A, B, C = map(int, input().split())
  print(min(A, C, floor((A + B + C) / 3)))