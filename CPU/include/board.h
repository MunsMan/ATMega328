#ifndef _BOARD_H_
#define _BOARD_H_

#include "types.h"
#include "cpu.h"
#include "operation.h"

#define SIZE_DATA 0x8FF
#define START_IO 0x20
#define START_EXT_IO 0x60
#define START_SRAM 0x100

byte_t read_byte(cpu_t* cpu, addr_t addr);
word_t read_word(cpu_t* cpu, addr_t addr);

void write_byte(cpu_t* cpu, addr_t addr, byte_t value);
void write_word(cpu_t* cpu, addr_t addr, word_t value);

instruction_t nextInstruction(cpu_t* cpu);

// Executes one Instruction
// returns number of clock cycles
int execute(cpu_t* cpu);

#endif  // _BOARD_H_