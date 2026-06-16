from pwn import * 

#nc playstation_hacking.chall.bytethecookies.org 5151

io = remote("playstation_hacking.chall.bytethecookies.org", 5151)

io.interactive()

# btc{buff3r_ov3rflow_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa}