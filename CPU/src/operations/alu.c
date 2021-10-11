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

void adc(cpu_t* cpu, instruction_t instruction){
    byte_t rd = cpu->r[getRd(instruction)];
    byte_t rr = cpu->r[getRr(instruction)];
    bit_t C = getC(cpu);
    byte_t r = rd + rr + C;

    cpu->r[getRd(instruction)] = r;

    bit_t rd3 = (rd >> 3) & 1;
    bit_t rd7 = (rd >> 7) & 1;
    bit_t rr3 = (rr >> 3) & 1;
    bit_t rr7 = (rr >> 7) & 1;
    bit_t r3 = (r >> 3) & 1;
    bit_t r7 = (r >> 7) & 1;

    (rd3 && rr3) || (rr3 && !r3) || (!r3 && rd3) ? setH(cpu) : clearH(cpu);
    (rd7 && rr7 && !r7) || (!rd7 && !rr7 && r7) ? setV(cpu) : clearV(cpu);
    r7 ? setN(cpu) : clearN(cpu);
    getN(cpu) ^ getV(cpu) ? setS(cpu): clearS(cpu);
    r == 0 ? setZ(cpu) : clearZ(cpu);
    (rd7 && rr7) || (rr7 && !r7) || (!r7 && rd7) ? setC(cpu) : clearC(cpu);

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

    r7 ? setN(cpu) : clearN(cpu);
    r == 0 ? setZ(cpu) : clearZ(cpu);
    (rd7 && rr7) || (rr7 && !r7 )|| (!r7 && rd7) ? setC(cpu) : clearC(cpu);
    (rd7 && rr7 && !r7) || (!rd7 && !rr7 && r7) ? setV(cpu) : clearV(cpu);
    getN(cpu) ^ getV(cpu) ? setS(cpu) : clearS(cpu);
    (rd3 && rr3) || (rr3 && !r3) || (!r3 && rd3) ? setH(cpu) : clearH(cpu);
}

void and_(cpu_t* cpu, instruction_t instruction){
    byte_t rd = cpu->r[getRd(instruction)];
    byte_t rr = cpu->r[getRr(instruction)];
    byte_t r = rd & rr;

    cpu->r[getRd(instruction)] = r;
    clearV(cpu);
    ((r >> 7) & 1) == 1 ? setN(cpu) : clearN(cpu);
    getN(cpu) ? setS(cpu) : clearS(cpu);
    r == 0 ? setZ(cpu) : clearZ(cpu);
}


reg_t getRd(instruction_t instruction){
    return (instruction >> 4) & 0x1F;
}

reg_t getRr(instruction_t instruction){
    return (instruction & 0xF) + ((instruction >> 5) & 0x10);
}