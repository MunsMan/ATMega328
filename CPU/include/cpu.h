#ifndef _CPU_H_
#define _CPU_H_

#include "avr_memory.h"

#define BOOT_ADDR 0x3FFF
#define NUM_REGISTER 32
#define SIZE_IO 64
#define SIZE_EXT_IO 160

typedef struct sreg {
    bit_t C: 1;
    bit_t Z: 1;
    bit_t N: 1;
    bit_t V: 1;
    bit_t S: 1;
    bit_t H: 1;
    bit_t T: 1;
    bit_t I: 1;
} sreg_t;

typedef struct cpu {
    reg_t r[NUM_REGISTER];
    sreg_t* sreg;
    byte_t io[SIZE_IO];
    byte_t ext_io[SIZE_EXT_IO];
    memory_t* memory;
    addr_t PC;
    uint64_t clock_cycles;
} cpu_t;


cpu_t* init_cpu(memory_t* memory);
void destroy_cpu(cpu_t* cpu);

byte_t read_io(cpu_t* cpu, addr_t addr);
byte_t read_ext_io(cpu_t* cpu, addr_t addr);

void write_io(cpu_t* cpu, addr_t addr, byte_t byte);
void write_ext_io(cpu_t* cpu, addr_t addr, byte_t byte);

bit_t getC(cpu_t* cpu);
bit_t getZ(cpu_t* cpu);
bit_t getN(cpu_t* cpu);
bit_t getV(cpu_t* cpu);
bit_t getS(cpu_t* cpu);
bit_t getH(cpu_t* cpu);
bit_t getT(cpu_t* cpu);
bit_t getI(cpu_t* cpu);

void setC(cpu_t* cpu);
void setZ(cpu_t* cpu);
void setN(cpu_t* cpu);
void setV(cpu_t* cpu);
void setS(cpu_t* cpu);
void setH(cpu_t* cpu);
void setT(cpu_t* cpu);
void setI(cpu_t* cpu);

void clearC(cpu_t* cpu);
void clearZ(cpu_t* cpu);
void clearN(cpu_t* cpu);
void clearV(cpu_t* cpu);
void clearS(cpu_t* cpu);
void clearH(cpu_t* cpu);
void clearT(cpu_t* cpu);
void clearI(cpu_t* cpu);

instruction_t fetch(cpu_t* cpu);

void increase_pc(cpu_t* cpu);

#endif //_CPU_H_