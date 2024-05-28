SLIB   := libvoid.so
TARGET := libevil.so

CC     := gcc

.PHONY: all
all: $(TARGET)

$(TARGET): $(SLIB)
	./make_evil.py $<
	mv $(addsuffix .mod, $<) $@

$(SLIB): 
	$(CC) $(CFLAGS) -shared -fPIC /dev/null -o $@

.PHONY: clean
clean:
	$(RM) $(TARGET) $(SLIB)

.PHONY: run
run: $(TARGET)
	# /lib64/ld-linux-x86-64.so.2 --list ./$(TARGET)
	setarch -R ldd ./$(TARGET)
