# epbpf-101

`epbpf-101` is a Go-based project that demonstrates the use of eBPF (Extended Berkeley Packet Filter) for packet counting. This project includes both the eBPF C code and the Go code required to load and interact with the eBPF program.

## Prerequisites

- Linux kernel version 5.7 or later, for bpf_link support
- LLVM 11 or later 1 (clang and llvm-strip)
- libbpf headers 2
- Linux kernel headers 3
- Go compiler version supported by ebpf-go's Go module

## Installation

1. **Clone the Repository**:

   ```sh
   git clone https://github.com/krishanthisera/epbpf-101.git
   cd epbpf-101
   ```

2. **Generate Go Bindings**: Use go generate to create Go bindings for the eBPF object file:

   ```sh
   go generate
   ```

3. **Build the Go Code**:

   ```sh
   go build
   ```

4. **Run the Go Code**:

   ```sh
   sudo ./epbpf-101
   ```
