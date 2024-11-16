#!/usr/bin/python
from bcc import BPF

# Define the eBPF program
program = r"""
int hello(void *ctx) {
// Get current user ID: https://docs.ebpf.io/linux/helper-function/bpf_get_current_uid_gid/
u32 uid = bpf_get_current_uid_gid() & 0xFFFFFFFF;

// Print the trace message
bpf_trace_printk("Hello World! UID: %d", uid);
return 0;
}
"""

# Load the eBPF program
b = BPF(text=program)
# execve: https://man7.org/linux/man-pages/man2/execve.2.html
syscall = b.get_syscall_fnname("execve")
b.attach_kprobe(event=syscall, fn_name="hello")
b.trace_print()


