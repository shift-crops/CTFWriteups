#include <stdio.h>
#include <time.h>

unsigned int _rand(void);

int main(void) {
	int i;
    
	setbuf(stdout, NULL);
	srand(time(NULL));

	while(1) {
		char c;
		c = getchar();

		if(c^'n')
			printf("%d\n", _rand());
		else
			break;
	}

	return 0;
}

unsigned int _rand(void){
	rand();
	__asm__(
		"cdq \n\t"
		"shr $0x1e, %edx \n\t"
		"add %edx, %eax \n\t"
		"and $0x3, %eax\n\t"
		"sub %edx, %eax\n\t"
	);

	return;
}
