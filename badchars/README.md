# Challenge 5: badchars
Steps:
- Find offset to RSP by sending a large cyclic to the program then using GDB to find the value stored in RSP. Once find the value stored in RSP, take the first four bytes which in this case was "kaaa", then use the command cyclic -l “kaaa” to find the offset. In this case it was 40.
- We are told that the program prints the bad chars upon running it. We can run the program using the command ./badchars in which we then see that the bad chars are 'x', 'g', 'a', '.'. See screenshot below:
![image](https://github.com/tylerdionne/ROPEMPORIUM2023/assets/143131384/3a97a931-64cc-495e-ac5d-1c28de9ae5f5)
- We know that similar to the previous challenge we want to write a string to memory and call print_file(). The issue in this challenge is flag.txt contains all of the bad chars.
- The way to get around this issue is using xor the string and then use gadgets to change it back once it is in memory.
- 
