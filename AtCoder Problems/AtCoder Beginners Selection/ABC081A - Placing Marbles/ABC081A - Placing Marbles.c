#include <stdio.h>

int main(){
  char s[4];
  scanf("%s", s);

  int answer = 0;

  for (int i = 0; i < 3; i++) {
    if (s[i] == '1') {
      answer++;
    }
  }
  
  printf("%d\n", answer);
  return 0;
}