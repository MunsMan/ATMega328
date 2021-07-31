#include "cpu.h"

sreg_t* init_sreg();


cpu_t* init_cpu(memory_t* memory){
    cpu_t* cpu = (cpu_t*)malloc(sizeof(cpu_t));
    cpu->sreg = init_sreg();
    cpu->memory = memory;
    cpu->PC = BOOT_ADDR;
    cpu->clock_cycles = 0;
    return cpu;
}

sreg_t* init_sreg(){
    sreg_t* sreg = (sreg_t*)malloc(sizeof(sreg_t));
    sreg->C = 0;
    sreg->Z = 0;
    sreg->N = 0;
    sreg->V = 0;
    sreg->S = 0;
    sreg->H = 0;
    sreg->T = 0;
    sreg->I = 0;
    return sreg;
}

void destroy_cpu(cpu_t* cpu){
    free(cpu->sreg);
    destroy_memory(cpu->memory);
    free(cpu);
}

byte_t read_io(cpu_t* cpu, addr_t addr){
    return cpu->io[addr];
}

byte_t read_ext_io(cpu_t* cpu, addr_t addr){
    return cpu->ext_io[addr];
}

void write_io(cpu_t* cpu, addr_t addr, byte_t byte){
    cpu->io[addr] = byte;
}

void write_ext_io(cpu_t* cpu, addr_t addr, byte_t byte){
    cpu->ext_io[addr] = byte;
}

bit_t getC(cpu_t* cpu){
    return cpu->sreg->C;
}
bit_t getZ(cpu_t* cpu){
    return cpu->sreg->Z;
}
bit_t getN(cpu_t* cpu){
    return cpu->sreg->N;
}
bit_t getV(cpu_t* cpu){
    return cpu->sreg->V;
}
bit_t getS(cpu_t* cpu){
    return cpu->sreg->S;
}
bit_t getH(cpu_t* cpu){
    return cpu->sreg->H;
}
bit_t getT(cpu_t* cpu){
    return cpu->sreg->T;
}
bit_t getI(cpu_t* cpu){
    return cpu->sreg->I;
}

void setC(cpu_t* cpu){
    cpu->sreg->C = true;
}

void setZ(cpu_t* cpu){
    cpu->sreg->Z = true;
}

void setN(cpu_t* cpu){
    cpu->sreg->N = true;
}

void setV(cpu_t* cpu){
    cpu->sreg->V = true;
}

void setS(cpu_t* cpu){
    cpu->sreg->S = true;
}

void setH(cpu_t* cpu){
    cpu->sreg->H = true;
}

void setT(cpu_t* cpu){
    cpu->sreg->T = true;
}

void setI(cpu_t* cpu){
    cpu->sreg->I = true;
}

void clearC(cpu_t* cpu){
    cpu->sreg->C = false;
}

void clearZ(cpu_t* cpu){
    cpu->sreg->Z = false;
}

void clearN(cpu_t* cpu){
    cpu->sreg->N = false;
}

void clearV(cpu_t* cpu){
    cpu->sreg->V = false;
}

void clearS(cpu_t* cpu){
    cpu->sreg->S = false;
}

void clearH(cpu_t* cpu){
    cpu->sreg->H = false;
}

void clearT(cpu_t* cpu){
    cpu->sreg->T = false;
}

void clearI(cpu_t* cpu){
    cpu->sreg->I = false;
}

instruction_t fetch(cpu_t* cpu){
    return read_flash(cpu->memory, cpu->PC);
}

void increase_pc(cpu_t* cpu){
    cpu->PC++;
}