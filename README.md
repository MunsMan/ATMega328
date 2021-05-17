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

This Project container his own Assembly Compiler/Assembler.
The Compiler works in 4 Steps:
1. Parsing Labels
2. Parsing Lines
3. Linking Labels
4. Compiling Code

### List of supported Instructions:
|Instruction|Meaning|example|
|:---:|:---:|:---:|
|ADD| Adding register or constants together| ADD r1 #5 |
|MOV| Move Register or Constants to another Register | MOV r5 #45 |