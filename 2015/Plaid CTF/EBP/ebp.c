#include<stdio.h>

int echo(void);
int make_response(void);

char buf[0x400];
char response[0x400];

int main(void){
	int r;

	while(1){
		r = (int)fgets(buf,0x400,stdin);
		if(r)
			echo();
		else
			break;
	}

	return r;
}

int echo(void){
	make_response();
	puts(response);
	return fflush(stdout);
}

int make_response(void){
	return snprintf(response,0x400,buf);
}
