#ifndef _BOARD_H_
#define _BOARD_H_

#include "types.h"
#include "cpu.h"

byte_t read_byte(addr_t addr);
word_t read_word(addr_t addr);

bool write_byte(addr_t addr, byte_t value);
bool write_word(addr_t addr, word_t value);

instruction_t fetch(cpu_t* cpu);

// Executes one Instruction
// returns number of clock cycles
int execute(cpu_t* cpu);

#endif  // _BOARD_H_