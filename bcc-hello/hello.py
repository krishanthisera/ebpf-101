#!/usr/bin/python
from bcc import BPF

# Define the eBPF program written in C
program = r"""
int hello(void *ctx) {
  // Get current user ID
  //  https://docs.ebpf.io/linux/helper-function/bpf_get_current_uid_gid/
  u32 uid = bpf_get_current_uid_gid() & 0xFFFFFFFF;

  // Print the trace message to the trace log of the kernel
  //  https://docs.ebpf.io/linux/helper-function/bpf_trace_printk/
  bpf_trace_printk("Hello World! UID: %d", uid);
return 0;
}
"""

# Load the eBPF program
b = BPF(text=program)
# execve: https://man7.org/linux/man-pages/man2/execve.2.html
syscall = b.get_syscall_fnname("execve")
# Blog article on linux tracing: https://jvns.ca/blog/2017/07/05/linux-tracing-systems/
b.attach_kprobe(event=syscall, fn_name="bcc-hello")
b.trace_print()
