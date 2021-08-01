#include "cpu.h"
#include "operations/alu.h"

reg_t getRd(instruction_t instruction);
reg_t getRr(instruction_t instruction);
void add(cpu_t* cpu, instruction_t instruction);

operation_t* alu(instruction_t instruction, operation_t* operation){
    instruction = instruction & 0xFF;
    operation->clock_cycles = 1;
    operation->operation = add;
    return operation;
}

void add(cpu_t* cpu, instruction_t instruction){
    byte_t rd = cpu->r[getRd(instruction)];
    byte_t rr = cpu->r[getRr(instruction)];
    byte_t r = rd + rr;

    cpu->r[getRd(instruction)] = r;
    
    bit_t rd3 = (rd >> 3) & 1;
    bit_t rd7 = (rd >> 7) & 1;
    bit_t rr3 = (rr >> 3) & 1;
    bit_t rr7 = (rr >> 7) & 1;
    bit_t r3 = (r >> 3) & 1;
    bit_t r7 = (r >> 7) & 1;

    rd < 0 ? setN(cpu) : clearN(cpu);
    rd == 0 ? setZ(cpu) : clearZ(cpu);
    rd7 * rr7 + rr7 * ~ r7 + ~r7 * rr7 ? setC(cpu) : clearC(cpu);
    rd7 * rr7 * ~r7 + ~rd7 * ~rr7 * r7 ? setV(cpu) : clearV(cpu);
    getN(cpu) ^ getV(cpu) ? setS(cpu) : clearS(cpu);
    rd3 * rr3 + rr3 * ~r3 + ~r3 * rd3 ? setH(cpu) : clearH(cpu);
}

reg_t getRd(instruction_t instruction){
    return (instruction >> 4) & 0x1F;
}

reg_t getRr(instruction_t instruction){
    return (instruction & 0xF) + ((instruction >> 5) & 0x10);
}