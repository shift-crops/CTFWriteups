global cursor_x, cursor_y
extern print, fdd_read

BITS 32

start:
	push msg
	call print
	add esp, 4

	mov ax, 0x100	; size
	mov bx, 0x1000	; address
	mov cx, 0x0011	; cylinder/sector
	mov dx, 0x0100	; head/drive
	call fdd_read

	push 0x1000
	call print
	add esp, 4

	hlt

msg:
	db "Flag is Here", 0x21, 0x21, 0x21, 0x0a, 0x00

cursor_x:
	dw 0
cursor_y:
	dw 1
