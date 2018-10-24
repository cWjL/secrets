#include <stdio.h>
#include <string.h>

int main(){
    char *scrt = "DOOSH\n";
    char usr_pw[20];
    printf("Enter the password: ");
    fgets(usr_pw,15,stdin);

    if(strcmp(usr_pw, scrt) == 0){
        printf("Correct!\n");
    }else{
        printf("Incorrect!\n");
        return 1;
    }
    return 0;
}