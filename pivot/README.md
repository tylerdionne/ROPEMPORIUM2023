# Challenge 7: pivot 
Steps:
- Find offset to RSP by sending a large cyclic to the program then using GDB to find the value stored in RSP. Once find the value stored in RSP, take the first four bytes which in this case was "kaaa", then use the command cyclic -l “kaaa” to find the offset. In this case it was 40.
- The goal of this challenge is to perform a "stack pivot" which simply means to move the stack pointer somewhere else in memory where you have your ROP chain. This is used when you are not given enough room to have your full ROP chain on the stack and have to create your ROP chain somewhere else in memory and pivot the stack pointer to that location.
- An important piece of information we are given is "This challenge imports a function named foothold_function() from a library that also contains a ret2win() function".
- So we know that we want to call the ret2win function but this is in the libppivot shared object which is not imported so we have to use ROP to call it.
- We also know that we are not given enough room on the stack to construct our full rop chain to do this. The program priints out a memory address that we can pivot to when ran. See screenshot below:
![image](https://github.com/tylerdionne/ROPEMPORIUM2023/assets/143131384/cc3306d0-e403-44f2-91e1-8e58d85747ba)
- This gives us valuable information. We now know we want to perfrom a stack pivot to that memory address, send our full rop chain, and then send our stack pivot rop.
- Therefore we must take in the address printed by the program each time and store that as the address we want to pivot the stack to.
- We can now start constructing our first payload which will pivot the stack. 



