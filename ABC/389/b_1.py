from math import factorial

X = int(input())

for i in range(100000):
  if factorial(i) == X:
    print(i)
    exit()