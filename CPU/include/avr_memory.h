#ifndef _MEMORY_H_
#define _MEMORY_H_

#include "types.h"

#define SIZE_SRAM 1048
#define SIZE_FLASH 18176

typedef struct memory memory_t;

memory_t* init_memory();
bool destroy_memory(memory_t* memory);

byte_t read_sram(memory_t* memory, addr_t addr);
instruction_t read_flash(memory_t* memory, addr_t addr);

void write_sram(memory_t* memory, addr_t addr, byte_t byte);
void write_flash(memory_t* memory, addr_t addr, instruction_t word);

bool check_addr_sram(memory_t* memory, addr_t addr);
bool check_addr_flash(memory_t* memory, addr_t addr);

void erase_memory(memory_t* memory);
bool flash_memory(memory_t* memory, char* filename);

size_t sram_size(memory_t* memory);
size_t flash_size(memory_t* memory);

#endif // _MEMORY_H