#include <stdio.h>

int main(){
  int N;
  scanf("%d", &N);

  int A[N];
  for(int i = 0; i < N; i++){
    scanf("%d", &A[i]);
  }

  long answer = 0;

  while(1){
    for(int i = 0; i < N; i++){
      if (A[i] % 2 == 1){
        printf("%ld\n", answer);
        return 0;
      }
    }
    for(int i = 0; i < N; i++){
      A[i] /= 2;
    }
    answer++;
  }
}