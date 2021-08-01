#include "board.h"

byte_t read_byte(cpu_t* cpu, addr_t addr){
    if(addr >= SIZE_DATA){
        fprintf(stderr, "ADDR not in DATA Space!\nADDR: %0.4X\n", addr);
        exit(EXIT_FAILURE);
    }
    if(addr < START_IO){
        return cpu->r[addr];
    } else if(addr < START_EXT_IO){
        return read_io(cpu, addr - START_IO);
    } else if(addr < START_SRAM){
        return read_ext_io(cpu, addr - START_EXT_IO);
    } else {
        return read_sram(cpu->memory, addr - START_SRAM);
    }
}

word_t read_word(cpu_t* cpu, addr_t addr){
    word_t word = (word_t)read_byte(cpu, addr+1) << 8;
    word |= (word_t)read_byte(cpu, addr);
    return word;
}

void write_byte(cpu_t* cpu, addr_t addr, byte_t value){
    if(addr >= SIZE_DATA){
        fprintf(stderr, "ADDR not in DATA Space!\nADDR: %0.4X\n", addr);
        exit(EXIT_FAILURE);
    }
    if(addr < START_IO){
        cpu->r[addr] = value;
    } else if(addr < START_EXT_IO){
        write_io(cpu, addr - START_IO, value);
    } else if(addr < START_SRAM){
        write_ext_io(cpu, addr - START_EXT_IO, value);
    } else {
        write_sram(cpu->memory, addr - START_SRAM, value);
    }
}

void write_word(cpu_t* cpu, addr_t addr, word_t value){
    write_byte(cpu, addr, value & 0xF);
    write_byte(cpu, addr+1, (value >> 8) & 0xF);
}

instruction_t nextInstruction(cpu_t* cpu){
    instruction_t instruction = fetch(cpu);
    increase_pc(cpu);
    return instruction;
}

int execute(cpu_t* cpu){
    instruction_t instruction = nextInstruction(cpu);
    operation_t operation;
    decodeInstruction(instruction, &operation);
    operation.operation(cpu, instruction);
    return operation.clock_cycles;
}