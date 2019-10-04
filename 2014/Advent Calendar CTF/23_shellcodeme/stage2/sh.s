bits 64
global _start

_start:
        mov rbx, '/bin/sh'
        push rbx
        mov rdi, rsp
	xor rsi, rsi
	xor rdx, rdx
	xor rax,rax
        mov al, 0x3b
        syscall
