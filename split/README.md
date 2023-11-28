# Challenge 2: split
Steps:
- Find offset to RSP by sending a large cyclic to the program then using GDB to find the value stored in RSP. Once find the value stored in RSP, take the first four bytes which in this case was "kaaa", then use the command cyclic -l “kaaa” to find the offset. In this case it was 40.
- Once again we can use radare2 to analyze the binary. Using the commands r2 split > aaa > afl we can see a list of the functions in the binary. here we see a usefulFunction. We can look at what is going on in this function using the command s sym.usefulFunction > pdf which shows us that the command system() is used here. This is useful to us because we can use this command in our exploit. See the screenshot below:
  ![image](https://github.com/tylerdionne/ROPEMPORIUM2023/assets/143131384/865547ac-39bd-45a2-9bf5-042356218d15)
- Now we want to look for strings in the binary that might be useful to us. More specifically we want to find some type of string that we can put inside of the system() command that will help us display the flag.
- To search for strings in the binary and grab the memory address of these strings we can use radare2. Using the command
'r2 -c "izz | grep flag" split' we find the string '/bin/cat flag.txt' is present in the binary at the address 0x00601060. See 
the screenshot below:
![image](https://github.com/tylerdionne/ROPEMPORIUM2023/assets/143131384/c99b7765-e966-45d1-9697-b6cef4a2bb51)
- Now we know we want to execute the command system('/bin/cat flag.txt'). We can achieve this in the following way. In the fastcall calling covention arguments are passed as registers. RDI is the first argument to a function. Given that the system() command only takes one argument we must populate the RDI register with our string '/bin/cat flag.txt'. We can do this via a pop rdi; ret; gadget.
- We can find gadgets in the binary using ropper. With the command 'ropper -f split | grep rdi' we see that we do in fact have a pop rdi; ret; gadget at the memory address 0x00000000004007c3. See the screenshot below:
![image](https://github.com/tylerdionne/ROPEMPORIUM2023/assets/143131384/c1c21640-450d-43f2-901f-92082ddeb042)
- One more gadget we need to include in our rop chain is a plain ret;. This is because of the fact that some functions like system() use the movaps instruction which requires the stack to be divisible by 16. So we can achieve this by just adding another 8 bytes to the stack with a ret;. We find this using ropper once again with the command 'ropper -f split | grep ret'
which will show we have a ret gadget at the address 0x000000000040053e.
- Now we can construct our ROP chain in the following way [pop rdi; ret; > location of '/bin/cat flag.txt' > ret; for alignment > address for system()]
- Upon running the program we retrieve the flag:
![image](https://github.com/tylerdionne/ROPEMPORIUM2023/assets/143131384/37dea7ad-2887-423f-b7c2-4d171dd7d629)

See the solution at: split.py
  
