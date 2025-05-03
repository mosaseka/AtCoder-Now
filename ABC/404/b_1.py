N = int(input())
S = [list(input()) for _ in range(N)]
T = [list(input()) for _ in range(N)]
MIN = [0, 1, 2, 3]

def rotate_90(matrix):
  return [[matrix[N - 1 - j][i] for j in range(N)] for i in range(N)]

rotations = [S]
for _ in range(3):
  rotations.append(rotate_90(rotations[-1]))

for i in range(4):
  COUNT = 0
  for j in range(N):
    for k in range(N):
      if rotations[i][j][k] != T[j][k]:
        COUNT += 1
  MIN[i] += COUNT

print(min(MIN))