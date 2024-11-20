# eBPF 101

The repository contains the learning materials for eBPF 101 presentation.

## Environment setup

Required packages: clang, llvm, libelf-dev, libpcap-dev, build-essential, make, linux-tools-common, gcc-multilib, libbpf-dev, python3

To install the required packages, run the following commands:

```bash
  apt install -y clang \ 
    llvm \ 
    libelf-dev \ 
    libpcap-dev \ 
    build-essential \ 
    make \ 
    linux-tools-common
```

**Note:** `gcc-multilib` is not currently available for ARM architectures. Instead, add `/usr/include/$(shell uname -m)-linux-gnu` into the include path. For more information, see [this thread](https://patchwork.ozlabs.org/project/netdev/patch/20200311123421.3634-1-tklauser@distanz.ch/).

```bash
  apt install -y gcc-multilib libbpf-dev
```

## Acknowledgement

- [Learning eBPF](https://isovalent.com/books/learning-ebpf/1098135121) by Liz Rice.
- [Diogo Daniel's blog article](https://diogodanielsoaresferreira.github.io/ebpf/)
- [Brendan Gregg's blog article](http://www.brendangregg.com/blog/2019-01-01/learn-ebpf-tracing.html)
