#ifndef _AVR_MEMORY_H
#define _AVR_MEMORY_H

#include "Register.h"
#include "Types.h"

#define FLASH_SIZE 16000
#define FLASH_OFFSET 0x8FF
#define IO_SIZE 64
#define EXT_IO_SIZE 160
#define SRAM_SIZE 1048

typedef struct memory_t memory_t;
typedef struct SRAM SRAM;

memory_t* init_memory(gpr_t* gpr);
SRAM* init_sram(gpr_t* gpr);
void sramFree(SRAM* sram);
void memoryFree(memory_t* mem);
byte_t readByte(memory_t* mem, addr_t addr);
word_t readWord(memory_t* mem, addr_t addr);

void writeByte(memory_t* mem, addr_t addr, byte_t value);
void writeWord(memory_t* mem, addr_t addr, word_t value);

// EEPROM
#define EEPROM_SIZE 0x0400

#define EEARH 0x22
#define EEARL 0x21
#define EEDR 0x20
#define EECR 0x1F

typedef struct EEPROM EEPROM;

#define EEPM1 5
#define EEPM0 4
#define EERIE 3
#define EEMPE 2
#define EEPE 1
#define EERE 0

// EEPROM FLAGS

#define EE_E 0x10 // Erase only
#define EE_W 0x20 // Write only
#define EE_R 0x30 // Reserve

EEPROM* init_eeprom();
void eepromFree(EEPROM* eeprom);
void write_eeprom(memory_t* mem);
byte_t read_eeprom(memory_t* mem);

#endif // _AVR_MEMORY_H