A,B,C,D,E = map(int,input().split())
LIST = ["ABCDE","BCDE","ACDE","ABDE","ABCE","ABCD","CDE","BDE","ADE",
        "BCE","ACE","BCD","ABE","ACD","ABD","ABC","DE","CE","BE","CD","AE","BD","AD","BC","AC","AB","E","D","C","B","A",]
ANSWER = []
CHECK = 0

for i in range(len(LIST)):
  CHECK = 0
  for j in range(len(LIST[i])):
    if LIST[i][j] == "A":
      CHECK += A
    elif LIST[i][j] == "B":
      CHECK += B
    elif LIST[i][j] == "C":
      CHECK += C
    elif LIST[i][j] == "D":
      CHECK += D
    elif LIST[i][j] == "E":
      CHECK += E
  ANSWER.append([LIST[i], CHECK])

ANSWER.sort(key=lambda x: (-x[1], x[0]))

for i in range(len(ANSWER)):
  print(ANSWER[i][0])