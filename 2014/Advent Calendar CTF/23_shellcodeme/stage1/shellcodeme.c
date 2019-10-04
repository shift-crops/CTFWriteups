/* gcc -m32 -fno-stack-protector -znoexecstack -o shellcodeme shellcodeme.c */
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>

#define SHELLCODE_LEN 1024

int main(void) {
    char *buf;
    buf = mmap((void *)0x20000000, SHELLCODE_LEN, PROT_READ|PROT_WRITE|PROT_EXEC, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
    read(0, &buf, SHELLCODE_LEN);
    mprotect((void *)0x20000000, SHELLCODE_LEN, PROT_READ); // no no no~
    (*(void(*)()) buf)(); // SEGV! no exec. can you execute shellcode?
}
