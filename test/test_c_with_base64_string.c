#include <stdio.h>
#include <string.h>
// secrets.py test binary source
char *get_super_duper(char*);

int main(void){
  char buff[5];
  char *secret_no_pad = "eW91ciBtb20K"; //"your mom"
  char *secret_with_pad = "eW91ciBtb20gCg=="; //"your mom "
  char *super_secret = "MTg2Mzk5MzA1NWQ3ZGJlYzkxMGZmODAwYzViODA5ZmMgIC0K"; // "your mom" | md5sum | base64
  //echo "secret string..shh" | base64 >> c2VjcmV0IHN0cmluZy4uc2hoCg==  with '==' removed
  char super_duper_secret[29] = "c2VjcmV0IHN0cmluZy4uc2hoCg";

  printf("Hello! Enter 'p' for padded, 'n' for no pad, or 's' for super secret: \n");
  fgets(buff,4,stdin);
  
  if(buff[0] == 'p'){
    printf("Secret with padding: %s", secret_with_pad);
    printf("\n");
  }else if(buff[0] == 'n'){
    printf("Secret without padding: %s", secret_no_pad);
    printf("\n");
  }else if(buff[0] == 's'){
    printf("Super secret: %s", super_secret);
    printf("\n");
  }else{
    printf("you're a fucking moron aren't you?\n");
  }
  printf(get_super_duper(super_duper_secret));
  printf("\n");
  return 0;
}

char *get_super_duper(char *str){
  return strcat(str, "==");
}
  
