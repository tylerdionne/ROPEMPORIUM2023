# Challenge 3: callme
Steps:
- Find offset to RSP by sending a large cyclic to the program then using GDB to find the value stored in RSP. Once find the value stored in RSP, take the first four bytes which in this case was "kaaa", then use the command cyclic -l “kaaa” to find the offset. In this case it was 40.
- As discussed in the previous challenge, in the fastcall calling covention arguments are passed as registers. RDI is the first argument to a function, RSI is the second argument to a function, and RDX is the 3rd argument to a function.
- In the instructions we are told the goal of this challenge si to make consecutive calls to a function from our ROP chain without crashing.
- We are also told that we must call the callme_one(), callme_two() and callme_three() functions in that order each with the arguments (0xdeadbeefdeadbeef, 0xcafebabecafebabe, 0xd00df00dd00df00d) and this will print the flag.
- To do this the first thing we want to find is a gadget that will allow us to set these three arguments to the function. Knowing now that the first three arguments to a function are RDI, RSI and RDX we want to look for a gadget with these registers. Using the command ropper -f callme | grep rdi we find that we have a gadget pop rdi; pop rsi; pop rdx; ret; at the address 0x000000000040093c. See screenshot:
![image](https://github.com/tylerdionne/ROPEMPORIUM2023/assets/143131384/1c26aca8-8b30-45f3-9afd-e3abecf341f7)
- Now we can construct our rop chain and set up each function call like so [pop rdi; pop rsi; pop rdx; ret; > arg_1 > arg_2 > arg_3 > function_1/2/3]
- Upon running the program we retrieve the flag:
![image](https://github.com/tylerdionne/ROPEMPORIUM2023/assets/143131384/270350c5-c4de-48fd-8edf-665308ecbdb0)

See the solution at: callme.py


