#ifndef __BPF_HELPER_H
#define __BPF_HELPER_H

#include <linux/bpf.h>

extern char bpf_log_buf[];
extern int bpf_log_level;

int bpf_create_map(enum bpf_map_type map_type, size_t value_size, unsigned int max_entries);
int bpf_lookup_elem(int fd, uint32_t key, void *value);
int bpf_update_elem(int fd, uint32_t key, const void *value, uint64_t flags);
int bpf_delete_elem(int fd, uint32_t key);
int bpf_prog_load(enum bpf_prog_type type, const struct bpf_insn *insns, int insn_cnt);

#endif
