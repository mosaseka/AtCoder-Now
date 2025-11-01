import sys
input = sys.stdin.readline

T = int(input())
RESULT = []

for i in range(T):
  A = input().strip()
  B = input().strip()

  if len(A) != len(B):
    RESULT.append(-1)
    continue
  AA = A + A
  IDX = AA.find(B)

  if 0 <= IDX < len(A):
    RESULT.append(IDX)
  else:
    RESULT.append(-1)

print("\n".join(map(str, RESULT)))