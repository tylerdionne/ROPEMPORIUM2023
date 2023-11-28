# Challenge 5: badchars
Steps:
- Find offset to RSP by sending a large cyclic to the program then using GDB to find the value stored in RSP. Once find the value stored in RSP, take the first four bytes which in this case was "kaaa", then use the command cyclic -l “kaaa” to find the offset. In this case it was 40.
- We are told that the program prints the bad chars upon running it. We can run the program using the command ./badchars in which we then see that the bad chars are 'x', 'g', 'a', '.'. See screenshot below:
![image](https://github.com/tylerdionne/ROPEMPORIUM2023/assets/143131384/3a97a931-64cc-495e-ac5d-1c28de9ae5f5)
- We know that similar to the previous challenge we want to write a string to memory and call print_file(). The issue in this challenge is flag.txt contains all of the bad chars.
- The way to get around this issue is using xor the string and then use gadgets to change it back once it is in memory.
- For this challenge we will use the .bss segment at 0x00601038 instead of the .data segment which we found once again using r2 badchars > aaa > iS.
- We now need to find gadgets that will help us to write our xor'd string to memory and then convert it back to the plaintext once it is in memory.
- First we need to find gadgets to write the ciphertext to the writeable memory. Using the command 'ropper -f badchars' we see that we have a pop r12; pop r13; pop r14; pop r15; ret; at 0x000000000040069c and a mov qword ptr [r13], r12; ret; at 0x0000000000400634. We can use the gadgets to write the ciphertext to memory. We then see we have a pop r14; pop r15; ret; at 0x00000000004006a0 and a xor byte ptr [r15], r14b; ret; at 0x0000000000400628. We can use these to xor each byte of the ciphertext back to the plaintext ('flag.txt') while in memory.
- We also need a pop rdi; ret; to set the first argument to print_file(). We can use roppper to find that we have this gadget at 0x4006a3.
- Now that we have all of the gadgets we need we can set up our ROP chain in the following manner [ pop r12; pop r13; pop r14; pop r15; ret; > r12 = xor'd string > r13 = writeable memory > r14 = 0 > r15 = 0 > mov qword ptr [r13], r12; > for loop through each character of ciphertext at writeable memory > pop r14; pop r15; ret; > r14 = number we xor'd by > r15 = writeable memory + current character position > xor byte ptr [r15], r14b; ret; > pop rdi; ret > rdi = writeable memory > print_file()]
- Running the program we retrieve the flag:
![image](https://github.com/tylerdionne/ROPEMPORIUM2023/assets/143131384/50caa3e3-423d-4597-9046-ecaa4d72c7bd)

See the solution at: badchars.py

