#include <stdio.h>
#include <string.h>

unsigned long decXORShift_R(unsigned long,int);

int main(void){
	int i;
	char flag[] = {0x71,0x22,0x49,0x14,0x6f,0x24,0x1d,0x31,0x65,0x1a,0x50,0x4a,0x1a,0x73,0x72,0x38,0x4d,0x17,0x3f,0x7f,0x79,0x0c,0x2b,0x11,0x5f,0x47,0x00};
	int len = strlen(flag);

	for(i=len-1; i>=0; i--){
		flag[i]=decXORShift_R(flag[i],1);
		flag[i]=decXORShift_R(flag[i],2);
		flag[i]=decXORShift_R(flag[i],3);
		flag[i]=decXORShift_R(flag[i],4);
		if(i>0)
			flag[i] ^= flag[i-1];
	}
	printf("%s",flag);

	return 0;
}

unsigned long decXORShift_R(unsigned long x,int t){
	unsigned long y=x, z=0;
	for(unsigned long mask=((1U<<t)-1)<<(sizeof(long)*8-t);mask;mask>>=t){
		z |= (y&mask)>>t;
		y = z^x;
	}
	return y;
}
