#ifndef _OPERATION_H_
#define _OPERATION_H_

#include "types.h"
#include "cpu.h"

typedef struct operation {
    unsigned clock_cycles;
    void (*operation)(cpu_t* cpu, instruction_t instruction);
} operation_t;

operation_t* decodeInstruction(instruction_t instruction, operation_t* operation);

#endif  // _OPERATION_H_