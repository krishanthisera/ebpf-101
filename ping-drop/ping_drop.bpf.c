#include <linux/bpf.h>
#include <bpf/bpf_helpers.h>
#include <linux/if_ether.h>
#include <linux/ip.h>
#include <linux/in.h>

struct
{
  // Generic array map type
  //  https://docs.kernel.org/bpf/map_array.html
  __uint(type, BPF_MAP_TYPE_ARRAY);
  __type(key, __u32);
  __type(value, __u64);
  __uint(max_entries, 1);
} icmp_counter SEC(".maps");

SEC("xdp")
int ping_drop(struct xdp_md *ctx)
{
  __u32 key = 0;
  // https://docs.ebpf.io/linux/helper-function/bpf_map_lookup_elem/
  __u64 *count = bpf_map_lookup_elem(&icmp_counter, &key);

  void *data = (void *)(long)ctx->data; // start of packet data
  void *data_end = (void *)(long)ctx->data_end; // end of packet data

  struct ethhdr *eth = data; // ethernet header
  struct iphdr *iph = data + sizeof(*eth); // ip header

  // check if packet has ip header
  if (data + sizeof(struct ethhdr) + sizeof(struct iphdr) > data_end)
  {
      return XDP_DROP;
  }

  // check if packet is ICMP
  if ( iph->protocol != IPPROTO_ICMP )
  {
      return XDP_PASS;
  }

  if (count) // Make verifier happy
  {
    // An atomic operation to increment the counter
    //   https://gcc.gnu.org/onlinedocs/gcc/_005f_005fsync-Builtins.html
    __sync_fetch_and_add(count, 1);
  }

  // Drop the packet and print the count
  bpf_printk("ping_drop: Dropped ICMP packet [%d]", count ? *count : 0);
  return XDP_DROP;
}

// verifier also checks that if we are using a BPF helper function that’s licensed
// There are some helper functions that are GPL-only, and some that are under the GPL-compatible license
char _license[] SEC("license") = "GPL";
