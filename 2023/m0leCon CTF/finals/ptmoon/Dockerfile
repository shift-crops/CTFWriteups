FROM ubuntu:23.10

COPY qemu-8.1.1-patched /build

WORKDIR /build
RUN apt-get update && apt-get install -y wget xz-utils git libglib2.0-dev libfdt-dev libpixman-1-dev zlib1g-dev ninja-build meson libslirp-dev python3-venv flex bison
RUN ./configure --enable-slirp --enable-debug && cd build && make -j

COPY flag.txt /flag.txt

ENTRYPOINT /build/build/qemu-system-x86_64 -enable-kvm -cdrom '/img/ubuntu-23.10.1-desktop-amd64.iso' -monitor none -serial stdio -net nic,model=virtio -net user -device vmware-svga -m 2048M -smp 2 -vnc 0.0.0.0:0
