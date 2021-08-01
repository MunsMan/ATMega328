#include "operations/branch.h"

operation_t* branch(instruction_t instruction, operation_t* operation){
    instruction++;
    return operation;
}