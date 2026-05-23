N = int(input())
S_LIST = list(map(str, input().split()))

ANSWER = ""

for i in range(N):
  if S_LIST[i][0] == "a" or S_LIST[i][0] == "b" or S_LIST[i][0] == "c":
    ANSWER += "2"
  elif S_LIST[i][0] == "d" or S_LIST[i][0] == "e" or S_LIST[i][0] == "f":
    ANSWER += "3"
  elif S_LIST[i][0] == "g" or S_LIST[i][0] == "h" or S_LIST[i][0] == "i":
    ANSWER += "4"
  elif S_LIST[i][0] == "j" or S_LIST[i][0] == "k" or S_LIST[i][0] == "l":
    ANSWER += "5"
  elif S_LIST[i][0] == "m" or S_LIST[i][0] == "n" or S_LIST[i][0] == "o":
    ANSWER += "6"
  elif S_LIST[i][0] == "p" or S_LIST[i][0] == "q" or S_LIST[i][0] == "r" or S_LIST[i][0] == "s":
    ANSWER += "7"
  elif S_LIST[i][0] == "t" or S_LIST[i][0] == "u" or S_LIST[i][0] == "v":
    ANSWER += "8"
  elif S_LIST[i][0] == "w" or S_LIST[i][0] == "x" or S_LIST[i][0] == "y" or S_LIST[i][0] == "z":
    ANSWER += "9"

print(ANSWER)