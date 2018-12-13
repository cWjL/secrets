#include <stdio.h>
#include <string.h>
#include <stddef.h>

char *decode(char *s){
  for(int i = 0; i < strlen(s); i++){
    s[i] ^= 0x15;
  }
  return s;
}

int main(int argc, char *argv[]){
  char secret[] = "}aaef/::lz`a`;wp:qDb!b,BrMvD";
  printf("Here is an encoded string %s\n\n", secret);
  printf("Here is a decoded string %s\n\n", decode(secret));
  return 0;
}
