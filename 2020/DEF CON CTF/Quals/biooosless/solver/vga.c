#include <stdint.h>

#define WIDTH	(0x50)
#define HEIGHT	(0x19)

extern uint16_t cursor_x, cursor_y;

uint32_t print(const uint8_t *s){
	uint32_t i;
	uint32_t *vmem = (uint32_t*)0xfd000000;

	for(i=0; s[i]; i++){
		vmem[cursor_y*WIDTH + cursor_x] = 0x0700 + s[i];
		cursor_x++;
		if(cursor_x >= WIDTH || !(s[i]^0x0a)){
			for(uint32_t j = cursor_x; j<WIDTH; j++)
				vmem[cursor_y*WIDTH + j] = 0x0720;
			cursor_x = 0;
			cursor_y++;
		}

		if(cursor_y >= HEIGHT){
			uint32_t j;
			for(j=0; j<(HEIGHT-1)*WIDTH; j++)
				vmem[j] = vmem[WIDTH+j];
			for(; j<HEIGHT*WIDTH; j++)
				vmem[j] = 0x0720;
			cursor_x = 0;
			cursor_y--;
		}
	}

	return i;
}
