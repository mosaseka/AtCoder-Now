N, K = map(int, input().split())
S = str(input())
LIST = []
COUNT = 0
QUE = ["",0,0]
ANSWER = ""
ZERO = 0

for i in range(N):
  if i == 0:
    QUE[0] = S[i]
    QUE[1] += 1
  else:
    if S[i] != S[i-1]:
      if S[i-1] == "1":
        COUNT += 1
        QUE[2] = COUNT
      LIST.append(QUE)
      QUE = [S[i],1,0]
    else:
      QUE[1] += 1

if S[-1] == "1":
  COUNT += 1
  QUE[2] = COUNT
LIST.append(QUE)
print(LIST)

k_index = -1
k_minus_1_index = -1

for i in range(len(LIST)):
    if LIST[i][2] == K:
        k_index = i
    elif LIST[i][2] == K - 1:
        k_minus_1_index = i

if k_index != -1 and k_minus_1_index != -1 and k_index > k_minus_1_index:
    element = LIST.pop(k_index)
    LIST.insert(k_minus_1_index + 1, element)

print(LIST)