package main

import (
	"log"
	"net"
	"os"
	"os/signal"
	"time"

	"github.com/cilium/ebpf/link"
	"github.com/cilium/ebpf/rlimit"
)

func main() {
	// Remove resource limits for kernels <5.11.
	// Linux kernels before 5.11 use RLIMIT_MEMLOCK
	// to control the maximum amount of memory allocated for a process' eBPF resources.
	// By default, it's set to a relatively low value.
	if err := rlimit.RemoveMemlock(); err != nil {
		log.Fatal("Removing memlock:", err)
	}

	// Load the compiled eBPF ELF and load it into the kernel.
	var objs counterObjects
	if err := loadCounterObjects(&objs, nil); err != nil {
		log.Fatal("Loading eBPF objects:", err)
	}
	defer objs.Close()

	ifname := "lo"
	iface, err := net.InterfaceByName(ifname)
	if err != nil {
		log.Fatalf("Interface %s not found: %v", ifname, err)
	}

	// Attach the eBPF program to the interface.
	link, err := link.AttachXDP(link.XDPOptions{
		Program:   objs.CountPackets,
		Interface: iface.Index,
	})
	if err != nil {
		log.Fatalf("Attaching XDP program: %v", err)
	}
	defer link.Close()

	log.Printf("Counting packets on %s\n", ifname)

	tick := time.Tick(time.Second)
	stop := make(chan os.Signal, 5)
	signal.Notify(stop, os.Interrupt)
	for {
		select {
		case <-tick:
			var count uint64
			err := objs.PktCounter.Lookup(uint32(0), &count)
			if err != nil {
				log.Fatalf("Map Lookup failed: %v", err)
			}
			log.Printf("Received %d packets\n", count)
		case <-stop:
			log.Print("Interrupted, exiting...")
			return
		}
	}

}
