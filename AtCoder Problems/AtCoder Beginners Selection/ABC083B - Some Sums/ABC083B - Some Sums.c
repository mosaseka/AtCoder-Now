#include <stdio.h>

int main(){
  int N, A, B;
  scanf("%d %d %d", &N, &A, &B);

  long answer = 0;

  for (int i = 1; i <= N; i++){
    int sum = 0;
    int n = i;
    while (n > 0){
      sum += n % 10;
      n /= 10;
    }
    if (sum >= A && sum <= B){
      answer += i;
    }
  }
  printf("%ld\n", answer);
  return 0;
}