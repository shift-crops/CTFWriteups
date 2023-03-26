#include <stdint.h>
#include <unistd.h>
#include <sys/syscall.h>
#include <linux/bpf.h>

int bpf_log_level;
char bpf_log_buf[0x1000];

static int bpf(enum bpf_cmd cmd, union bpf_attr *attr){
    return syscall(__NR_bpf, cmd, attr, sizeof(*attr));
}

int bpf_create_map(enum bpf_map_type map_type, size_t value_size, unsigned int max_entries){
	union bpf_attr attr = {
		.map_type    = map_type,
		.key_size    = sizeof(uint32_t),
		.value_size  = value_size,
		.max_entries = max_entries
	};

	return bpf(BPF_MAP_CREATE, &attr);
}

int bpf_lookup_elem(int fd, uint32_t key, void *value){
	union bpf_attr attr = {
		.map_fd = fd,
		.key    = (uint64_t)&key,
		.value  = (uint64_t)value,
	};

	return bpf(BPF_MAP_LOOKUP_ELEM, &attr);
}

int bpf_update_elem(int fd, uint32_t key, const void *value, uint64_t flags){
	union bpf_attr attr = {
		.map_fd = fd,
		.key    = (uint64_t)&key,
		.value  = (uint64_t)value,
		.flags  = flags,
	};

	return bpf(BPF_MAP_UPDATE_ELEM, &attr);
}

int bpf_delete_elem(int fd, uint32_t key){
	union bpf_attr attr = {
		.map_fd = fd,
		.key    = (uint64_t)&key,
	};

	return bpf(BPF_MAP_DELETE_ELEM, &attr);
}

int bpf_prog_load(enum bpf_prog_type type, const struct bpf_insn *insns, int insn_cnt){
	union bpf_attr attr = {
		.prog_type = type,
		.insn_cnt  = insn_cnt,
		.insns     = (uint64_t)insns,
		.license   = (uint64_t)"GPL",
		.log_level = bpf_log_level,
		.log_size  = sizeof(bpf_log_buf),
		.log_buf   = (uint64_t)bpf_log_buf,
	};

	return bpf(BPF_PROG_LOAD, &attr);
}
