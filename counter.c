//go:build ignore

#include <linux/bpf.h>
#include <bpf/bpf_helpers.h>

struct
{
  __unit(type, BPF_MAP_TYPE_ARRAY);
  __unit(key, __u32);
  __unit(value, __u64);
  __unit(max_entries, 1);
} pkt_counter SEC(".maps");

SEC("xdp")
int count_packets()
{
  __u32 key = 0;
  __u64 *count = bpf_map_lookup_elem(&pkt_counter, &key);
  if (count)
  {
    // atomically increment the counter
    __sync_fetch_and_add(count, 1);
  }
  return XDP_PASS;
}

char __license[] SEC("license") = "Dual MIT/GPL"; 


