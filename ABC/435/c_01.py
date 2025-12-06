N = int(input())
A = list(map(int, input().split()))
ANSWER = 1
NOW = 2
END = 1 + A[0]

while NOW <= N and NOW < END:
  ANSWER += 1
  END = max(END, NOW + A[NOW - 1])
  NOW += 1

print(ANSWER)