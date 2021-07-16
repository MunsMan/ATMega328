# Implementation of an ATMEGA328

**State** = *building*

This is mainly a educational Project, be build a good fundation of the functioning of an CPU. Most of the process is live Streamed on [Twitch](https://www.twitch.tv/cmunsman). You are welcome to support this Project and add you Ideas and Code to it. Because the goal is, to be as close to the acutal CPU, we will follow the official Documentation.

## Emulator

The Emulator is build around the official ATMega328 Documentation. The goal of the Emulator is, to run AVG Instruction on you main Machine before flashing it on the Chip itself. A later goal is, to add a Web interface, to visually debug or observe the CPU running.

### Run it locally

Sadly, at the moment there is no easy way added to execute Instruction. It will follow soon.

## Compiler / Assembler

This Project container his own Assembly Compiler/Assembler.
The Compiler works in 4 Steps:
1. Parsing Labels
2. Parsing Lines
3. Linking Labels
4. Compiling Code

To Learn more, check the [Compiler1](https://github.com/MunsMan/ATMega328/tree/Compiler/compiler1) out.
