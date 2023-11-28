# Challenge 4: write4
Steps:
- Find offset to RSP by sending a large cyclic to the program then using GDB to find the value stored in RSP. Once find the value stored in RSP, take the first four bytes which in this case was "kaaa", then use the command cyclic -l “kaaa” to find the offset. In this case it was 40.
- In this challenge the goal is to call print_file('flag.txt'). We are told that the print_file() command is present in the binary but 'flag.txt' is not.
- The way around this is the following. We must find a writeable region of memory and write the string 'flag.txt' to this piece of memory so we can use it. We can do this using gadgets.
- 
