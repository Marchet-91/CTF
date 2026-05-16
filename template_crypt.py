import subprocess
from pwn import *

def sage(expr):
    return subprocess.check_output(
        ["sage", "-c", expr],
        text=True
    ).strip()

