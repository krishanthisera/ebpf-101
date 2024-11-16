PROG = ping_drop
TARGETS = ${PROG}
DEV = lo

all: $(TARGETS)
.PHONY: all

$(TARGETS): %: %.bpf.o

%.bpf.o: %.bpf.c
	clang \
	    -target bpf \
		-I/usr/include/$(shell uname -m)-linux-gnu \
		-g \
	    -O2 -o $@ -c $<

clean:
		- rm *.bpf.o
		- rm -f /sys/fs/bpf/${PROG}

load: all unload
	- bpftool prog load ${PROG}.bpf.o /sys/fs/bpf/${PROG}

attach: detach
	- bpftool net attach xdp pinned /sys/fs/bpf/${PROG} dev ${DEV}

detach:
	- bpftool net detach xdp dev ${DEV}

unload: detach
	- rm -f /sys/fs/bpf/${PROG}

show-dev:
	- ip link show dev ${DEV}

