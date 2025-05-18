T = str(input())
U = str(input())
INDEX= []
ALPHABET = [chr(ord("a") + i) for i in range(26)]

for i in range(len(T)):
  if T[i] == "?":
    INDEX.append(i)

for i in ALPHABET:
  for j in ALPHABET:
    for k in ALPHABET:
      for l in ALPHABET:
        CHECK = list(T)
        CHECK[INDEX[0]] = i
        CHECK[INDEX[1]] = j
        CHECK[INDEX[2]] = k
        CHECK[INDEX[3]] = l
        CHECK = "".join(CHECK)
        if U in CHECK:
          print("Yes")
          exit()

print("No")