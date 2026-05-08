#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int compare(const void *a, const void *b){
  return (*(int*)b - *(int*)a);
}

int main(){
  int N;
  scanf("%d", &N);

  int a[N];
  for(int i = 0; i < N; i++){
    scanf("%d", &a[i]);
  }

  int Alice = 0, Bob = 0;

  qsort(a, N, sizeof(int), compare);

  for(int i = 0; i < N; i++){
    if(i % 2 == 0){
      Alice += a[i];
    } else {
      Bob += a[i];
    }
  }

  printf("%d\n", Alice - Bob);
  return 0;
}