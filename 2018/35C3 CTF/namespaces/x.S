global _start

_start:
	mov rdi, 1
	mov rsi, buf
	mov rdx, 6
	mov rax, 1
	syscall

	mov rdi, 0
	mov rsi, rsp
	mov rdx, 0x100
	mov rax, 0
	syscall

buf:
	db	"Hello",10
