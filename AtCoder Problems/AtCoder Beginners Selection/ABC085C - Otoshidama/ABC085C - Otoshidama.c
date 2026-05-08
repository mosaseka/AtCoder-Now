#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(){
  int N;
  long Y;
  scanf("%d %ld", &N, &Y);

  for(int i = 0; i <= N; i++){
    for(int j = 0; j <= N - i; j++){
      int k = N - i - j;
      if(10000 * i + 5000 * j + 1000 * k == Y){
        printf("%d %d %d\n", i, j, k);
        return 0;
      }
    }
  }
  printf("%d %d %d\n", -1, -1, -1);
  return 0;
}