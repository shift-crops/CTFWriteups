TARGET	= patch.bin
OBJS	= bios.o vga.o fdd.o

CC 	:= gcc
AS 	:= nasm
CFLAGS	+= -masm=intel -nostdlib -fno-asynchronous-unwind-tables -fno-pie -fno-stack-protector -m32
LDFLAGS	+= --entry=start --oformat=binary -Ttext 0x7fbd8a4 -melf_i386

all :
	make $(TARGET)

%.o : %.c
	$(CC) $(CFLAGS) -c $<

%.o : %.asm
	$(AS) -f elf $<

$(TARGET) : $(OBJS)
	$(LD) $(LDFLAGS) -o $@ $(OBJS)

clean:
	$(RM) $(OBJS) $(TARGET)
