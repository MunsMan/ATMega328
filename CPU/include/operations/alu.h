#ifndef _OPERATIONS_ALU_H_
#define _OPERATIONS_ALU_H_

#include "operation.h"

operation_t* alu(instruction_t instruction, operation_t* operation);

void adc(cpu_t* cpu, instruction_t instruction);
void add(cpu_t* cpu, instruction_t instruction);
void and(cpu_t* cpu, instruction_t instruction);

#endif  // _OPERATIONS_ALU_H_