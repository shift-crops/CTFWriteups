BITS 64
	lea rax, [rel $ + 0x12]
	push rax
	mov dword [rsp+4], 0x23
	retf

BITS 32
	nop

