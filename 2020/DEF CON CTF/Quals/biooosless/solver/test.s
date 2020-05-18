BITS 32
ORG 0x7fbd8a4

	mov edi, msghello
	call puts
	hlt

puts:
	pusha
	xor eax, eax
	mov esi, edi
	mov edi, 0xfd000000
	mov ah, 0x7
puts_loop:
	mov al, [esi]
	cmp al, 0
	je puts_end
	mov [edi], eax
	inc esi
	add edi, 4
	jmp puts_loop
puts_end:
	popa
	ret

msghello:
	db "1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890", 0x00
	db "Hello, World", 0x00

