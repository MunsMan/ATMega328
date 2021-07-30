#ifndef _CPU_H
#define _CPU_H

#include "AVRMemory.h"
#include "Operations.h"
#include "Register.h"
#include "Types.h"

#define MASK_2_OP 0b1111110000000000

cpu_t* initCPU();
void freeCPU(cpu_t* cpu);
void flashMemory(cpu_t* cpu, addr_t addr, instruction_t inst);
void execute(cpu_t* cpu, CLOCK_CYCLE clockCycle);
instruction_t fetch(cpu_t* cpu);

sreg_t* getSR(cpu_t* cpu);
gpr_t* getGPR(cpu_t* cpu);

void addPC(cpu_t* cpu, byte_t steps);
void subPC(cpu_t* cpu, byte_t steps);

void writeRegister(cpu_t* cpu, addr_t addr, byte_t value);
byte_t readRegister(cpu_t* cpu, addr_t addr);
word_t readMemory(cpu_t* cpu, addr_t addr);
void printGPRegister(cpu_t* cpu);

#endif //_CPU_H