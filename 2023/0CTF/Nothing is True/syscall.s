global open, close, mmap64, munmap, brk, execve, exit
global read, write, mmap32
extern addr_syscall

section .text

BITS 64
open:
	mov rax, 2
	call [addr_syscall]
	ret

close:
	mov rax, 3
	call [addr_syscall]
	ret

mmap64:
	mov rax, 9
	mov r10, rcx
	call [addr_syscall]
	ret

munmap:
	mov rax, 11
	call [addr_syscall]
	ret

brk:
	mov rax, 12
	call [addr_syscall]
	ret

execve:
	mov rax, 59
	call [addr_syscall]
	ret

exit:
	mov rax, 60
	call [addr_syscall]
	ret

read:
	push rbp
	call _conv_arg
	push _read32
	jmp _switch32

write:
	push rbp
	call _conv_arg
	push _write32
	jmp _switch32

mmap32:
	push rbp
	call _conv_arg
	push _mmap32
	jmp _switch32

_conv_arg:
	mov ebx, edi
	xchg esi, ecx
	mov edi, r8d
	mov ebp, r9d
	ret

_switch32:
	mov dword [rsp+4], 0x23
	retf

BITS 32
_read32:
	mov eax, 3
	push esp
	mov ebp, esp
	sysenter

_write32:
	mov eax, 4
	push esp
	mov ebp, esp
	sysenter

_mmap32:
	mov eax, 90
	push esp
	push ebp
	push edi
	push esi
	push edx
	push ecx
	push ebx
	mov ebx, esp
	lea ebp, [esp+0x18]
	sysenter

section .sysexit exec

_switch64:
	pop ebp
	push 0x33
	call $+5
	add dword [esp], 0x5
	retf
BITS 64
	pop rbp
	ret

_padding:
%rep 0xff8-(_padding-_switch64)
	nop
%endrep
	jmp _switch64
