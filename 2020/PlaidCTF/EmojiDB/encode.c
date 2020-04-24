#include <stdio.h>
#include <wchar.h>
#include <locale.h>

int enc_utf2uni(void){
	wchar_t buf[5] = {0};

	fgetws(buf, sizeof(buf)/sizeof(wchar_t), stdin);
	write(1, buf, sizeof(buf));
}

int enc_uni2utf(void){
	char buf[0x14] = {0};

	read(0, buf, sizeof(buf));
	fputws((wchar_t*)buf, stdout);
}

int main(int argc, char *argv[]){
	setbuf(stdout, NULL);
	setlocale(0, "en_US.UTF-8");

	while(1){
		char n = 0;

		write(1, "> ", 2);
		read(0, &n, sizeof(n));
		
		switch(n){
			case 1:
				enc_utf2uni();
				break;
			case 2:
				enc_uni2utf();
				break;
			default:
				return 0;
		}
		write(1, "Done\n", 5);
	}
}

