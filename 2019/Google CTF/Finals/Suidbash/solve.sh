#!./suidbash

enable -f ./swapuid.so swapuid
id -a
swapuid
id -a

exec /bin/bash -p
