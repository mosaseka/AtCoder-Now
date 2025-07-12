def GeneratePalindromes(MAX_VAL):
  PALINDROMES = []
  
  for i in range(1, 10):
    if i <= MAX_VAL:
      PALINDROMES.append(i)
  
  for LENGTH in range(2, len(str(MAX_VAL)) + 1):
    HALF_LENGTH = LENGTH // 2
    START = 10 ** (HALF_LENGTH - 1)
    END = 10 ** HALF_LENGTH
    
    for i in range(START, END):
      S = str(i)
      if LENGTH % 2 == 0:
        PALINDROME_STR = S + S[::-1]
      else:
        for MID in range(10):
          PALINDROME_STR = S + str(MID) + S[::-1]
          PALINDROME = int(PALINDROME_STR)
          if PALINDROME <= MAX_VAL:
            PALINDROMES.append(PALINDROME)
        continue
      
      PALINDROME = int(PALINDROME_STR)
      if PALINDROME <= MAX_VAL:
        PALINDROMES.append(PALINDROME)
  
  return sorted(PALINDROMES)

def ToBaseA(N, A):
  if N == 0:
    return [0]
  DIGITS = []
  while N > 0:
    DIGITS.append(N % A)
    N //= A
  return DIGITS[::-1]

def IsPalindromeBaseA(N, A):
  DIGITS = ToBaseA(N, A)
  return DIGITS == DIGITS[::-1]

A = int(input())
N = int(input())

DECIMAL_PALINDROMES = GeneratePalindromes(N)

TOTAL = 0
for NUM in DECIMAL_PALINDROMES:
  if IsPalindromeBaseA(NUM, A):
    TOTAL += NUM

print(TOTAL)