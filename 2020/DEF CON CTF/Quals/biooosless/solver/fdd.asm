global fdd_read

BITS 32

fdd_read:
	call set_dma

	xchg dh, ch
	xchg ch, cl
	shl ecx, 16
	mov cx, dx

	push 0xff2a1202
	push ecx
	call fdd_read_data
	add esp, 8

	mov dx, 0x03f5
	mov ecx, 0
read_status:
	in al, dx
	inc ecx
	cmp ecx, 7
	jl read_status

	ret

set_dma:
	push ecx
	push edx
	mov cx, ax

	; mask ch2
	mov dx, 0x000f
	mov al, 0x4
	out dx, al

	; base address
	mov dx, 0x0004
	mov al, bl
	out dx, al
	mov al, bh
	out dx, al

	; base count
	mov dx, 0x0005
	mov al, cl
	out dx, al
	mov al, ch
	out dx, al

	; set mode
	mov dx, 0x000b
	mov al, 0x16
	out dx, al

	; unmask ch2
	mov dx, 0x000f
	mov al, 0x0
	out dx, al

	pop edx
	pop ecx
	ret

fdd_read_data:
	push ebp
	mov ebp, esp
	mov dx, 0x03f5
	mov ax, 0x06
	out dx, al
	mov ecx, 0x08
	jmp fdd_args

fdd_args:
	push esi
	mov esi, 0
args_loop:
	cmp esi, ecx
	jge args_end
	mov al, [ebp+esi+8]
	out dx, al
	inc esi
	jmp args_loop
args_end:
	pop esi
	leave
	ret
