N = int(input())

ANSWER = 0

for i in range(N):
  A, B, S = map(str, input().split())
  A, B = int(A), int(B)
  match S:
    case "keep":
      ANSWER += B - A
    case "take":
      pass

print(ANSWER)