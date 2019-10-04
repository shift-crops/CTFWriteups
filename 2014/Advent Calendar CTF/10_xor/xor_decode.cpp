#include <stdio.h>
#include <string.h>

unsigned long decXORShift_R(unsigned long,int,unsigned long);

int main(void){
	int i;
	char flag[] = {0x71,0x22,0x49,0x14,0x6f,0x24,0x1d,0x31,0x65,0x1a,0x50,0x4a,0x1a,0x73,0x72,0x38,0x4d,0x17,0x3f,0x7f,0x79,0x0c,0x2b,0x11,0x5f,0x47,0x00};
	int len = strlen(flag);

	for(i=len-1; i>=0; i--){
		flag[i]=decXORShift_R(flag[i],1,0xff);
		flag[i]=decXORShift_R(flag[i],2,0xff);
		flag[i]=decXORShift_R(flag[i],3,0xff);
		flag[i]=decXORShift_R(flag[i],4,0xff);
		if(i>0)
			flag[i] ^= flag[i-1];
	}
	printf("%s",flag);

	return 0;
}

unsigned long decXORShift_R(unsigned long y,int t,unsigned long ad){
	unsigned long x;
	if(~ad){
		x=y&~ad;
		y=y&ad;
		for(unsigned long i=1<<(sizeof(long)*8-1);i;i>>=1)
			if(ad&i)
				x |= ((x>>t)^y)&i;
			else
				y |= (x^(x>>t))&i;
	}
	else{
		unsigned long z=0;
		x=y;
		for(unsigned long mask=((1U<<t)-1)<<(sizeof(long)*8-t);mask;mask>>=t){
			z |= (x&mask)>>t;
			x = z^y;
		}
	}
	return x;
}
