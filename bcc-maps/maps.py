#!/usr/bin/python
from asyncio import sleep
from bcc import BPF

# Kernel code: count the number of syscalls for each user
program = r"""
// BCC - Map to store the count of each syscall
//  https://github.com/iovisor/bcc/blob/master/docs/reference_guide.md#2-bpf_hash
BPF_HASH(syscalls_count);

int hello(void *ctx) {
  u64 uid;
  u64 counter = 0;
  u64 *p;

  // Get current user ID
  uid = bpf_get_current_uid_gid() & 0xFFFFFFFF;

  // BCC - Lookup the count of syscalls for the current user
  //  https://github.com/iovisor/bcc/blob/master/docs/reference_guide.md#19-maplookup
  p = syscalls_count.lookup(&uid);

  if (p != 0) {
    counter = *p;
  }

  counter++;
  // BCC - Update the count of syscalls
  //  https://github.com/iovisor/bcc/blob/master/docs/reference_guide.md#22-mapupdate
  syscalls_count.update(&uid, &counter);

  return 0;
}
"""


# User Space: eBPF program
b = BPF(text=program)
# execve: https://man7.org/linux/man-pages/man2/execve.2.html
syscall = b.get_syscall_fnname("execve")
# Blog article on linux tracing: https://jvns.ca/blog/2017/07/05/linux-tracing-systems/
b.attach_kprobe(event=syscall, fn_name="bcc-maps")


# Print the count of syscalls for each user
while True:
  sleep(2)
  s = ""
  if len(b["syscalls_count"]) > 0:
    for k, v in b["syscalls_count"].items():
      s += "UID: %d - Syscalls: %d\n" % (k.value, v.value)
    print(s)
  else:
    print("No syscalls yet")
