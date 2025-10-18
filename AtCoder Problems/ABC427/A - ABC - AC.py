S = str(input())
L = len(S)

print(S[:(L+1)//2-1] + S[(L+1)//2:])