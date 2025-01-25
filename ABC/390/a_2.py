A_LIST = list(map(int,input().split()))

if [A_LIST[1]] + [A_LIST[0]] + [A_LIST[2]] + [A_LIST[3]] + [A_LIST[4]] == list(sorted(A_LIST)):
  print("Yes")
elif [A_LIST[0]] + [A_LIST[2]] + [A_LIST[1]] + [A_LIST[3]] + [A_LIST[4]] == list(sorted(A_LIST)):
  print("Yes")
elif [A_LIST[0]] + [A_LIST[1]] + [A_LIST[3]] + [A_LIST[2]] + [A_LIST[4]] == list(sorted(A_LIST)):
  print("Yes")
elif [A_LIST[0]] + [A_LIST[1]] + [A_LIST[2]] + [A_LIST[4]] + [A_LIST[3]] == list(sorted(A_LIST)):
  print("Yes")
else:
  print("No")