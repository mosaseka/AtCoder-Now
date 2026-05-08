#include <stdio.h>

int main(){
  int a;
  scanf("%d", &a);

  int b, c;
  scanf("%d %d", &b, &c);

  char s[100];
  scanf("%s", s);

  printf("%d %s\n", a + b + c, s);

  return 0;
}