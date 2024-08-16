#!/bin/bash

/home/user/qemu-system-x86_64 \
	-L /home/user/bios \
	-kernel /home/user/bzImage \
	-initrd /home/user/rootfs.cpio.gz \
	-m 1024M \
	-append "console=ttyS0 oops=panic panic=1 quiet" \
	-nographic \
	-device nvme-subsys,id=nvme-subsys-0,nqn=subsys-0,fdp=on,fdp.nruh=128, \
	-device nvme,serial=1234,cmb_size_mb=64,subsys=nvme-subsys-0 \
	-drive file=null-co://,if=none,format=raw,id=nvm-1 \
	-device nvme-ns,drive=nvm-1,nsid=1,fdp.ruhs=0-63 \
	-device ich9-intel-hda,id=sound0,addr=0x1b \
	-device rtl8139 \
	-device rtl8139,netdev=net0 -netdev user,id=net0
