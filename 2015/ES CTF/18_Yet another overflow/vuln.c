#include <stdio.h>
#include <unistd.h>

int func(int a, int b, int c) {
  if(a != b) {
    return a+b*c;
  }
  asm("popq %rdi;ret;popq %rsi;ret;popq %rdx;ret;popq %rcx;ret");
}

void vuln(void) {
  char buf[512];
  write(1, "Let's Pwn!\n", func(2, 3, 3));
  read(0, buf, 1024);
  puts(buf);
}

int main(int ac, char **av) {
  setvbuf(stdout, NULL, _IONBF, 0);
  vuln();
  return 0;
}
