# Challenge 7: pivot 
Steps:
- Find offset to RSP by sending a large cyclic to the program then using GDB to find the value stored in RSP. Once find the value stored in RSP, take the first four bytes which in this case was "kaaa", then use the command cyclic -l “kaaa” to find the offset. In this case it was 40.
- The goal of this challenge is to perform a "stack pivot" which simply means to move the stack pointer somewhere else in memory where you have your ROP chain. This is used when you are not given enough room to have your full ROP chain on the stack and have to create your ROP chain somewhere else and pivot the stack pointer to that location.
- 
