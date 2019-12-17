// gcc -I/usr/include/bash -I/usr/include/bash/include swapuid.c -shared -o swapuid.so 
#include <builtins.h>
#include <unistd.h>
#include <stdio.h>

static void swapuid(void){
	uid_t ruid, euid, suid;

	getresuid(&ruid, &euid, &suid);
	if(euid != suid){
		setresuid(ruid, suid, euid);
		printf("swap euid(%d) <-> suid(%d)\n", euid, suid);
	}
	else
		printf("euid and suid are equal (%d)\n", euid);
}

struct builtin swapuid_struct = {
    "swapuid",
    swapuid,
    BUILTIN_ENABLED,
    "",
    "swap euid and suid",
    0,
};

