#include <stdio.h>
#include <inttypes.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#include <seccomp.h>
#include <linux/seccomp.h>
#include <unistd.h>
#include <sys/mman.h>
#include <stdlib.h>

int __attribute__((constructor)) setup()
{
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);

    scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_KILL);
    if (ctx == NULL)
    {
        printf("seccomp_init failed\n");
        return 1;
    }

    if (seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(open), 0) < 0 ||
        seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0) < 0 ||
        seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0) < 0 ||
        seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0) < 0 ||
        seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(rt_sigreturn), 0) < 0 ||
        seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(ioctl), 0) < 0 ||
        seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(getpid), 0) < 0 ||
        seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0) < 0)
    {
        printf("seccomp_rule_add failed\n");
        return 1;
    }

    if (seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(mmap), 1,
                         SCMP_A2(SCMP_CMP_MASKED_EQ, PROT_READ | PROT_WRITE, PROT_READ | PROT_WRITE)) < 0)
    {
        printf("seccomp_rule_add failed for mmap\n");
        return -1;
    }

    if (seccomp_load(ctx) < 0)
    {
        printf("seccomp_load failed\n");
        return 1;
    }

    seccomp_release(ctx);
    return 0;
}

struct memo {
	char *buf;
	int size;
};

int menu(void);
int scan(char *buf, int size);
int scanInt(void);
int main(void){
	struct memo m[16];

	for(;;){
		int menu, idx, size;
		menu = scanInt();
		if(!menu)
			return 0;

		idx = scanInt();
		switch(menu){
			case 1:
				m[idx].size = size = scanInt();
				m[idx].buf = malloc(size);
				break;
			case 2:
				printf(":> ");
				read(0, m[idx].buf, m[idx].size);
				break;
			case 3:
				write(1, m[idx].buf, m[idx].size);
				break;
			case 4:
				bzero(m[idx].buf, m[idx].size);
				free(m[idx].buf);
				break;
			default:
				exit(0);
		}
	}
}

int menu(void){
	printf("\n"
			"1. Add\n"
			"2. Edit\n"
			"3. View\n"
			"4. Delete\n");
	return scanInt();
}

int scan(char *buf, int size){
	int len;

	if(size <= 0 || (len = read(0, buf, size-1)) <= 0)
		return -1;

	if(buf[len-1]=='\n')
		len--;
	buf[len] = '\0';

	return len;
}

int scanInt(void){
	char buf[0x10] = {};

	printf(":> ");
	scan(buf, sizeof(buf));
	return strtoull(buf, NULL, 10);
}
