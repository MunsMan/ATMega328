#ifndef _OPERATIONS_H
#define _OPERATIONS_H

#include <stdio.h>

#include "ALU.h"
#include "Types.h"

#define TWO_OP_MASK
#define ONE_OP_MASK
#define ZERO_OP_MASK

typedef void (*operation_t)(cpu_t*, instruction_t);

operation_t getOperation(instruction_t instruction);
operation_t twoOperation(instruction_t instruction);
operation_t oneOperation(instruction_t instruction);
operation_t zeroOperation(instruction_t instruction);
operation_t registerImmediate(instruction_t instruction);
operation_t loadStore(instruction_t instruction);
operation_t basicOperation(instruction_t instruction);
operation_t conditionalBranch(instruction_t instruction);

addr_t getRd(instruction_t instruction);
addr_t getRr(instruction_t instruction);

void ldi(cpu_t* cpu, instruction_t instruction);
void nop(cpu_t* cpu, instruction_t instruction);

#endif // _OPERATIONS_H