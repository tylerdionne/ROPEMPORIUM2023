# Challenge 6: fluff
Steps:
- Find offset to RSP by sending a large cyclic to the program then using GDB to find the value stored in RSP. Once find the value stored in RSP, take the first four bytes which in this case was "kaaa", then use the command cyclic -l “kaaa” to find the offset. In this case it was 40.
- Once again the ultimate goal of this challenge is to call print_file('flag.txt'). The problem with this challenge is that we are not given any simple gadgets to accomplish this task.
- We know that we once again must write our string 'flag.txt' to memory so similar to challenge write4 we will use the .data segment at 0x0601029.
- Now we have to look at the gadgets we are given to work with. We are told that some useful gadgets are available at the questionableGadgets symbol.
- Using objdump -d fluff we can analyze this function. Here we see we have a few gadgets xlat; ret;, pop rdx pop rcx add rcx 0x3ef2 bextr rbx, rcx, rdx; ret;, and stos [rdi], al; ret;
![image](https://github.com/tylerdionne/ROPEMPORIUM2023/assets/143131384/7e4557a2-39da-4bed-b4ae-5529fc0b30e2)
- We now have to do some research on what these gadgets do because these are not common but we know we can use these to write our string into memory.
- xlatb ret; → uses AL contents to locate a entry in a table then copies the contents int hat table entry back to AL so it allows us to control the AL register 
- pop rdx pop rcx add rcx, 0x3ef2 bextr rbx, rcx, rdx; ret; → copies bits from the source register which is the second argument (in this case RCX) and copies them to the destination register (in this case RBX) and the third argument specifies the length so it allows us to control the RBX register.
- stosb byte [rdi], al; ret; → stores a byte from AL into RDI so it allows us to control RDI.
- In order to write our string to memory we first must find the location of each character in our string in the binary. Then we must use our gadgets to move each chatracter into rbx using bextr then moving the value in rbx into al using xlatb then using a pop rdi; ret; to set rdi to the writeable memory and finally using stosb to have rdi (writeable memory + character index) point at our charcter stored in al.
- Once our writeable memory is then pointing at our string ('flag.txt') we will then set rdi with a pop rdi; ret; then call print_file() just like the previous challenges.
- Upon running the program we retrieve the flag:
![image](https://github.com/tylerdionne/ROPEMPORIUM2023/assets/143131384/85e7d576-689c-4834-8624-989a2bd2ae25)

See the solution at: fluff.py
