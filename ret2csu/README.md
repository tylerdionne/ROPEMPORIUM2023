# Challenge 8: ret2csu
Steps:
- Find offset to RSP by sending a large cyclic to the program then using GDB to find the value stored in RSP. Once find the value stored in RSP, take the first four bytes which in this case was "kaaa", then use the command cyclic -l “kaaa” to find the offset. In this case it was 40.
- We are told that this challenge is similar to the callme challenge but without the useful gadgets. The instructions also make it clear that the difficult part of this challenge will be populating the third argument for the ret2win function. Recall the fastcall calling convetion in which RDI = first argument to a function, RSI = second argument to a function and RDX = third argument to a function.
- We are provided a link to 'https://i.blackhat.com/briefings/asia/2018/asia-18-Marco-return-to-csu-a-new-method-to-bypass-the-64-bit-Linux-ASLR-wp.pdf' which is very useful in devloping this exploit.
- This paper basically describes that there are two useful gadgets present in all bianries compiled with this library. In the __libc_csu_init function there are two gadgets that we can use to help us set the values of the first three arguements to a function call RDI, RSI, and RDX. So we will use these gadgets to help us set RDX in this challenge.
- The first thing we must do is find these gadgets in this function. Using the command ' objdump -d ret2csu' we can examine the dissasembly of the __libc_csu_init function. See screenshot below:
![image](https://github.com/tylerdionne/ROPEMPORIUM2023/assets/143131384/be78c095-ce85-49e2-a59c-46841e88205b)
- From this function we can get our two gadgets. Gadget one is at 0x40069a and includes pop rbx, pop rbp, pop r12, pop r13, pop r14, pop r15. This gadget helps set the registers that are used in gadget two. Gadget two is at 0x400680 and includes 
mov %r15,%rdx mov %r14,%rsi mov %r13d,%edi call *(%r12,%rbx,8) add $0x1,%rbx cmp %rbx,%rbp add $0x8,%rsp and then all of the pop instructions from gadget 1.
- We can now start constructing our ROP chain. First we call gadget 1 to set these registers. Keep in mind our arguments (arg_1 = 0xdeadbeefdeadbeef, arg_2 = 0xcafebabecafebabe, arg_3 = 0xd00df00dd00df00d). For the first two pop instructions (pop rbx and pop rbp) we want to set rbx to 0 and rbp to 1 so that the instruction 'cmp %rbx,%rbp' in gadget 2 is false. Then we want to set r12 to a pointer to a function that will not disturb rdx and rbx because recall that in gadget 2 we have a 'call *(%r12,%rbx,8)' instruction. A address we can store in r12 to ensure these values are not modified is a pointer to the _init function which can be found in the dynamic section of the binary. We can find this address using the command 'r2 ret2csu > aaa > s sym..dynamic > pd' and then navigate to the desired address which in this case is 0x00600e38. See screenshot below:
![image](https://github.com/tylerdionne/ROPEMPORIUM2023/assets/143131384/b18cb10f-71e2-483a-9c0d-712a23a94fd5)
- We then want to set r13, r14  and r15 to our 3 arguments because these registers will become RDI, RSI, and RDX respectively in gadget 2. We must keep in mind that the %r13d in the second gadget will only copy over half of the first argument so we will have to fix that later.
- We can then call gadget 2 and put 0 in add rsp, 0x8 and the other pop instructions. After that we have to grab a pop rdi; ret; instruction found at 0x4006a3 using ropper to make sure that the entirety of argument 1 is copied over. We can then call ret2win now that our registers are set to our desired arguments. The address of the ret2win function can be found using objdump -d ret2csu and navigating to usefulFunction where it is called. The address is 0x400510. See screenshot below:
![image](https://github.com/tylerdionne/ROPEMPORIUM2023/assets/143131384/11afcf99-da32-4720-8510-fb8838d81267)
- Running the program we retreive the flag:
![image](https://github.com/tylerdionne/ROPEMPORIUM2023/assets/143131384/26e5e946-7f59-423a-9928-6a952daff277)

See the solution at: ret2csu.py


