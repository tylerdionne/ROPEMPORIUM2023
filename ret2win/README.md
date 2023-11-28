# Challenge 1: ret2win
Steps:
- Find offset to RSP by sending a large cyclic to the program then using GDB to find the value stored in RSP. Once find the value stored in RSP, take the first four bytes which in this case was "kaaa", then use the command cyclic -l “kaaa” to find the offset. In this case it was 40.
- Using radare2 we can analyze the binary. Using the commands r2 ret2win > aaa > s sym.ret2win > pdf we see that the ret2win function displays the flag. See the screenshot below:
![image](https://github.com/tylerdionne/ROPEMPORIUM2023/assets/143131384/7a3c57fd-9b43-43dd-90ea-378131e44fb4)
- Knowing that this is the function we want to call, we can overwrite RSP with the address of this function.
- Upon running the program we retreive the flag:
![image](https://github.com/tylerdionne/ROPEMPORIUM2023/assets/143131384/1fba108a-2765-46e6-919e-8a3bd552f4c7)

See the solution at:
ret2win.py


