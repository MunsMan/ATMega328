#ifndef _ALU_H
#define _ALU_H

#include "CPU.h"
#include "Register.h"
#include "Types.h"

byte_t _add(sr_t* sr, byte_t rd, byte_t rr);

void add(cpu_t* cpu, instruction_t instruction);
void adc(cpu_t* cpu, instruction_t instruction);

void adiw(cpu_t* cpu, instruction_t instruction);
word_t _adiw(sr_t* sr, word_t Rd, byte_t k);

// logical And
void land(cpu_t* cpu, instruction_t instruction);

// logical And with Immediate
void andi(cpu_t* cpu, instruction_t instruction);

// base add operation
byte_t _and(sr_t* sr, byte_t Rd, byte_t Rr);

// Arithmetic Shift Operation
void asr(cpu_t* cpu, instruction_t instruction);

// Bit Clear in SREG
void bclr(cpu_t* cpu, instruction_t instruction);

// Bit Load from the T Flag in SREG to a Bit in Register
void bld(cpu_t* cpu, instruction_t instruction);

// Branch if Bit in SREG is cleared
void brbc(cpu_t* cpu, instruction_t instruction);

void sbiw(cpu_t* cpu, instruction_t instruction);

#endif // _ALU_H