# unzip nightmare.zip
# DOCKER_BUILDKIT=1 docker build -t nightmare .

FROM ubuntu@sha256:cc8f713078bfddfe9ace41e29eb73298f52b2c958ccacd1b376b9378e20906ef

COPY --chmod=755 lib/ld-linux-x86-64.so.2.debug /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
COPY --chmod=644 lib/libc.so.6.debug /usr/lib/x86_64-linux-gnu/libc.so.6
COPY --chmod=755 bin/nightmare /nightmare

ENTRYPOINT ["/nightmare"]
