N, X = map(str, input().split())
N = int(N)

INDEX = float("inf")

match X:
  case "A":
    INDEX = 0
  case "B":
    INDEX = 1
  case "C":
    INDEX = 2
  case "D":
    INDEX = 3
  case "E":
    INDEX = 4

for i in range(N):
  S = str(input())
  if S[INDEX] == "o":
    print("Yes")
    exit()

print("No")