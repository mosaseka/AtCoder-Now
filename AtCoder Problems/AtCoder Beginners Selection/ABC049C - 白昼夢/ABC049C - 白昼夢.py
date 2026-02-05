S = str(input())
S = S[::-1]

DIVIDE = ["dream", "dreamer", "erase", "eraser"]
for i in range(len(DIVIDE)):
  DIVIDE[i] = DIVIDE[i][::-1]

CAN = True
i = 0

while i < len(S):
  CAN2 = False
  for j in range(len(DIVIDE)):
    D = DIVIDE[j]
    if i + len(D) <= len(S) and S[i:i+len(D)] == D:
      CAN2 = True
      i += len(D)
      break
  if not CAN2:
    CAN = False
    break

if CAN:
  print("YES")
else:
  print("NO")