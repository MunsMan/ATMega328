#ifndef _OPERATION_H_
#define _OPERATION_H_

#include "types.h"

typedef struct operation {
    unsigned clock_cycles;
    void (*operation)(instruction_t instruction);
} operation_t;

operation_t* decodeInstruction(instruction_t instruction);

#endif  // _OPERATION_H_