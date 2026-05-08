#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void reverse(char *s) {
  int i = 0;
  int j = strlen(s) - 1;

  while (i < j) {
    char temp = s[i];
    s[i] = s[j];
    s[j] = temp;
    i++;
    j--;
  }
}

int main(void) {
  char S[100001];
  scanf("%s", S);

  char divide[4][8] = {"dream", "dreamer", "erase", "eraser"};
  for (int i = 0; i < 4; i++) {
    reverse(divide[i]);
  }
  reverse(S);

  int can = 1;
  int n = (int)strlen(S);

  for (int i = 0; i < n;) {
    int can2 = 0;
    for (int j = 0; j < 4; j++) {
      int len = (int)strlen(divide[j]);
      if (i + len <= n && strncmp(S + i, divide[j], len) == 0) {
        can2 = 1;
        i += len;
        break;
      }
    }
    if (!can2) {
      can = 0;
      break;
    }
  }

  if (can) {
    printf("YES\n");
  } else {
    printf("NO\n");
  }

  return 0;
}
