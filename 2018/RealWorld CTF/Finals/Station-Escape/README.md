# Station-Escape

## file

VMWare Workstation：
[VMware-Workstation-Full-15.0.2-10952284.x86_64.bundle](https://drive.google.com/open?id=1SlojAhX0NCpWTPjASfM03v5QBvRtT-sp)
[patched VMX](https://drive.google.com/open?id=1MJQSQYufGtl9DQnG1osyMk_1YbgCPL-E)

## exploit in vm

```
$ gcc exploit.c -masm=intel -DDEBUG -o exploit
$ ./exploit "DISPLAY=:0 xcalc"
```
