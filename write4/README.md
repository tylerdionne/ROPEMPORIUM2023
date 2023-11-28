# Challenge 4: write4
Steps:
- Find offset to RSP by sending a large cyclic to the program then using GDB to find the value stored in RSP. Once find the value stored in RSP, take the first four bytes which in this case was "kaaa", then use the command cyclic -l “kaaa” to find the offset. In this case it was 40.
- In this challenge the goal is to call print_file('flag.txt'). We are told that the print_file() command is present in the binary but 'flag.txt' is not.
- The way around this is the following. We must find a writeable region of memory and write the string 'flag.txt' to this piece of memory so we can use it. We can do this using gadgets.
- Upon looking at the dissasembly using the command objdump -d write4 we see a usefulGadgets function. After looking more closely at this function we see that we are given a mov[r14], r15 gadget at the memory address 0x400628. 

 400628:       4d 89 3e                mov    %r15,(%r14)
