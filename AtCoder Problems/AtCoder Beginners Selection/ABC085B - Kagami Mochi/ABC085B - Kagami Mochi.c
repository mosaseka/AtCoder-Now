#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int compare(const void *a, const void *b){
  return (*(int*)a - *(int*)b);
}

int array_unique(int* array, int size){
  int end = 0;
  for(int i = 1; i < size; i++){
    if (array[i] != array[end]){
      end++;
      array[end] = array[i];
    }
  }
  return end + 1;
}

int main(){
  int N;
  scanf("%d", &N);

  int d[101];
  for(int i = 0; i < N; i++){
    scanf("%d", &d[i]);
  }

  qsort(d, N, sizeof(int), compare);

  printf("%d\n", array_unique(d, N));
  return 0;
}