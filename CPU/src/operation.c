#include "operation.h"
#include "operations/alu.h"
#include "operations/branch.h"

operation_t* decodeInstruction(instruction_t instruction, operation_t* operation){
    if((instruction & 0xC000) == 0){
        return alu(instruction, operation);
    }
    if((instruction & 0xF800) == 0xF000){
        return branch(instruction, operation);
    }
    return NULL;
}