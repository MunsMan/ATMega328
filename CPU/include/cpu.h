#ifndef _CPU_H_
#define _CPU_H_

#include "memory.h"

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
    register_t r[NUM_REGISTER];
    sreg_t* sreg;
    byte_t io[SIZE_IO];
    byte_t ext_io[SIZE_EXT_IO];
    memory_t* memory;
    addr_t PC;
    addr_t SP;
    uint64_t clock_cycles;
} cpu_t;


cpu_t* init_cpu(memory_t* memory);
bool destroy_cpu(cpu_t* cpu);

byte_t read_io(addr_t addr);
byte_t read_ext_io(addr_t addr);

bool write_io(addr_t addr, byte_t byte);
bool write_ext_io(addr_t addr, byte_t byte);

bit_t getC(sreg_t* cpu);
bit_t getZ(sreg_t* cpu);
bit_t getN(sreg_t* cpu);
bit_t getV(sreg_t* cpu);
bit_t getS(sreg_t* cpu);
bit_t getH(sreg_t* cpu);
bit_t getT(sreg_t* cpu);
bit_t getI(sreg_t* cpu);

bool setC(sreg_t* cpu);
bool setZ(sreg_t* cpu);
bool setN(sreg_t* cpu);
bool setV(sreg_t* cpu);
bool setS(sreg_t* cpu);
bool setH(sreg_t* cpu);
bool setT(sreg_t* cpu);
bool setI(sreg_t* cpu);

#endif //_CPU_H_