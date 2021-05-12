# Implementation of an ATMEGA328

**State** = *building*

## Startup

At the moment, the original Startup Method is not implemented.

`SP` -> `0x08FF`
`PC` -> `0x0100`

ADD R0 R1
000011 0 00000 0001


LDI R0 #100 : R0 <- 100;

100 = 0b 0110 0100

 op  4bit  r   4bit
1110 0110 0000 0100


## Compiler / Assembler

At base there is a custom compiler for basic Assembly Code. This Compiler is writen in Python and takes `*.o`files. You can find the compiler in tehe `./compiler`directory.

### Constantes

At the moment only unsigned Constants are supported. At the moment I'm not sure if signed Constants are even allowed in real assembly.




Constant c = -50 -> 1100 1110
Word w = -8173 -> 1110 0000 0001 0011
wh = 1110 0000
wl = 0001 0011


    wl          0001 0011
    c           1100 1110
wl = wl + c ->  1110 0001
