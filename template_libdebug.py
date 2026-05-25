#!/usr/bin/env python3
from libdebug import debugger
import sys

def inversione(b):
    return -b & 0xff

# =========================
# CONFIG
# =========================
BINARY = "./CCIA"
ARGS = [] # argomenti
BREAKPOINTS = [ # Breakpoint
    0x1483
]

AUTO_GDB = False
VERBOSE_REGS = True


# =========================
# CALLBACKS
# =========================
def dump_info(thread, bp):
    print(f"\n[+] Breakpoint hit @ {hex(bp.address)}")
    regs = thread.regs

    if VERBOSE_REGS:
        print(f"RIP: {hex(regs.rip)}")
        print(f"RAX: {hex(regs.rax)}")
        print(f"RBX: {hex(regs.rbx)}")
        print(f"RCX: {hex(regs.rcx)}")
        print(f"RDX: {hex(regs.rdx)}")
        print(f"RSI: {hex(regs.rsi)}")
        print(f"RDI: {hex(regs.rdi)}")
        print(f"RSP: {hex(regs.rsp)}")

    # esempio lettura stack
    # try:
    #     stack = thread.memory[regs.rsp : regs.rsp + 0x40]
    #     print(f"[stack] {stack.hex()}")
    # except Exception as e:
    #     print(f"[!] Stack read failed: {e}")


# =========================
# HELPERS
# =========================
def dump_mem(thread, addr, size=0x40):
    data = thread.memory[addr: addr + size]
    print(f"\n[MEM {hex(addr)}]")
    print(data.hex())


def step_n(thread, n=1):
    for _ in range(n):
        thread.step()
        print(f"-> RIP: {hex(thread.regs.rip)}")


def find_char(thread, bp):
    rdx = thread.regs.rdx
    c = inversione(rdx)
    print(c)
    thread.regs.rdx

# =========================
# MAIN
# =========================
dbg = debugger([BINARY] + ARGS)
dbg.run()
print("Start1")

for b in BREAKPOINTS:
    dbg.breakpoint(BREAKPOINTS, callback=find_char)

print("Start")
dbg.c()