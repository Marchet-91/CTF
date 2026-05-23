import angr
import claripy

BINARY = "./chall"

# Load project
proj = angr.Project(BINARY, auto_load_libs=False)

# Input simbolico (32 bytes)
flag = claripy.BVS("flag", 8 * 32)

# Stato iniziale
state = proj.factory.entry_state(
    stdin=flag
)

# Vincoli ASCII printable
for i in range(32):
    byte = flag.get_byte(i)
    state.solver.add(byte >= 0x20)
    state.solver.add(byte <= 0x7e)

# Sim manager
simgr = proj.factory.simulation_manager(state)

# Cerca success/fail
SUCCESS_ADDR = 0x401234
FAIL_ADDR = 0x401250

simgr.explore(
    find=SUCCESS_ADDR,
    avoid=FAIL_ADDR
)

if simgr.found:
    found = simgr.found[0]
    solution = found.solver.eval(flag, cast_to=bytes)
    print("[+] Found:", solution)
else:
    print("[-] No solution")