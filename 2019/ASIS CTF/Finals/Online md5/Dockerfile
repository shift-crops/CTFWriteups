FROM ubuntu:17.04

RUN set -x && \
    sed -i -r 's/archive\.ubuntu\.com|security\.ubuntu\.com/old-releases.ubuntu.com/g' /etc/apt/sources.list && \
    dpkg --add-architecture i386 && \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y libc6:i386 libc6-dbg:i386 libssl1.0.0:i386 socat && \
    apt-get clean && rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/*

WORKDIR /root
COPY md5_online.elf . 
COPY banner.txt .

RUN	 chmod +x md5_online.elf

CMD ["socat","-v","tcp-listen:4296,reuseaddr,fork","exec:./md5_online.elf"]
