# Challenge 4: write4
Steps:
- Find offset to RSP by sending a large cyclic to the program then using GDB to find the value stored in RSP. Once find the value stored in RSP, take the first four bytes which in this case was "kaaa", then use the command cyclic -l “kaaa” to find the offset. In this case it was 40.
- In this challenge the goal is to call print_file('flag.txt'). We are told that the print_file() command is present in the binary but 'flag.txt' is not.
- The way around this is the following. We must find a writeable region of memory and write the string 'flag.txt' to this piece of memory so we can use it. We can do this using gadgets.
- Upon looking at the dissasembly using the command objdump -d write4 we see a usefulGadgets function. After looking more closely at this function we see that we are given a mov[r14], r15 gadget at the memory address 0x400628. This gadget stores the contents of r15 in the memory location pointed at by r14. Note that it looks backwards in the screenshot but this is only because it is in AT&T sytnax, it is still the same instruction. See screenshot below:
  ![image](https://github.com/tylerdionne/ROPEMPORIUM2023/assets/143131384/d6a88403-3c95-4451-a66d-1432232b0231)
- We will also need a gadget to set these registers. We use the command ropper -f write4 | grep r14 to find there is a pop r14; pop r15; ret; at the memory address 0x0000000000400690.
- Now all that we need to do is find a writeable region of memory. We can do this using radare2. Using the commands r2 write4 > aaa > iS we find that the .data segment has read and write permissions and is at the memory address 0x601028. Note that there are other writeable regions of memory shown here that could also be used. See screenshot below:
![image](https://github.com/tylerdionne/ROPEMPORIUM2023/assets/143131384/c4cc14a0-4035-434e-b5a9-5f9c292c0c36)
- Now the last thing we need is a pop rdi; ret; gadget to set the first argument to the print_file() command. Using the command 'ropper -f write4 | grep rdi' we find a pop rdi; ret; gadget at the memory address 0x400693.
-Now we can construct our ROP chain in the following manner [pop r14; pop r15; ret; > r14 = writeable memory > r15 = 'flag.txt' > mov[r14], r15 > pop rdi; ret; > writeable memory > print_file()]
-Upon running the program we retrieve the flag:
![image](https://github.com/tylerdionne/ROPEMPORIUM2023/assets/143131384/994da833-d1c2-4122-8cc5-7f3fd5c6740f)

See the solution at: write4.py

