/* gcc -m32 -fno-stack-protector -zexecstack -o oh_my_scanf oh_my_scanf.c */
#include <stdio.h>

int main(void) {
    char name[16];

    setvbuf(stdout, NULL, _IONBF, 0);
    printf("name: ");
    scanf("%s", name);
    printf("hi, %s\n", name);

    return 0;
}
