#include "AVRMemory.h"

typedef struct memory_t {
	word_t* flash;  // main Memory
	SRAM* sram;     // cpu cache / ram
	EEPROM* eeprom; // EEPROM
} memory_t;

typedef struct SRAM {
	gpr_t* gpr;
	byte_t* io;
	byte_t* extIO;
	byte_t* sram;
} SRAM;

memory_t* init_memory(gpr_t* gpr) {
	memory_t* mem = (memory_t*)malloc(sizeof(memory_t));
	mem->flash = (word_t*)malloc(sizeof(word_t) * FLASH_SIZE);
	mem->sram = init_sram(gpr);
	mem->eeprom = init_eeprom();
	return mem;
}

SRAM* init_sram(gpr_t* gpr) {
	SRAM* sram = (SRAM*)malloc(sizeof(SRAM));
	sram->io = (byte_t*)malloc(sizeof(byte_t) * IO_SIZE);
	sram->extIO = (byte_t*)malloc(sizeof(byte_t) * EXT_IO_SIZE);
	sram->sram = (byte_t*)malloc(sizeof(byte_t) * SRAM_SIZE);
	sram->gpr = gpr;
	return sram;
}
void sramFree(SRAM* sram) {
	gprFree(sram->gpr);
	free(sram->io);
	free(sram->extIO);
	free(sram->sram);
	free(sram);
}

void memoryFree(memory_t* mem) {
	sramFree(mem->sram);
	free(mem->flash);
	eepromFree(mem->eeprom);
	free(mem);
}

byte_t readByte(memory_t* mem, addr_t addr) {
	if(addr < 0x0020) {
		return gprReadByte(mem->sram->gpr, addr);
	} else if(addr < 0x0060) {
		return mem->sram->io[addr];
	} else if(addr < 0x00FF) {
		return mem->sram->extIO[addr];
	} else if(addr < 0x0500) {
		return mem->sram->sram[addr];
	} else if(addr < 0x3FFF) {
		return (byte_t)mem->flash[addr];
	}
	return 0x00;
}

word_t readWord(memory_t* mem, addr_t addr) {
	if(addr < 0x0020) {
		return gprReadWord(mem->sram->gpr, addr);
	} else if(addr < 0x0060) {
		return (word_t)mem->sram->io[addr + 1] << 8 | mem->sram->io[addr];
	} else if(addr < 0x00FF) {
		return (word_t)mem->sram->extIO[addr + 1] << 8 | mem->sram->extIO[addr];
	} else if(addr < 0x0500) {
		return (word_t)mem->sram->sram[addr + 1] << 8 | mem->sram->sram[addr];
	} else if(addr < 0x3FFF) {
		return mem->flash[addr];
	}
	return 0x00;
}

void writeByte(memory_t* mem, addr_t addr, byte_t value) {
	if(addr < 0x0020) {
		gprWriteByte(mem->sram->gpr, addr, value);
	} else if(addr < 0x0060) {
		mem->sram->io[addr] = value;
	} else if(addr < 0x00FF) {
		mem->sram->extIO[addr] = value;
	} else if(addr < 0x0500) {
		mem->sram->sram[addr] = value;
	} else if(addr < 0x3FFF) {
		mem->flash[addr] = value;
	}
}

void writeWord(memory_t* mem, addr_t addr, word_t value) {
	if(addr < 0x0020) {
		gprWriteWord(mem->sram->gpr, addr, value);
	} else if(addr < 0x0060) {
		mem->sram->io[addr] = (byte_t)value;
		mem->sram->io[addr + 1] = (word_t)value >> 8;
	} else if(addr < 0x00FF) {
		mem->sram->extIO[addr] = (byte_t)value;
		mem->sram->extIO[addr + 1] = (word_t)value >> 8;
	} else if(addr < 0x0500) {
		mem->sram->sram[addr] = (byte_t)value;
		mem->sram->sram[addr + 1] = (word_t)value >> 8;
	} else if(addr < 0x3FFF) {
		mem->flash[addr] = value;
	}
}

typedef struct EEPROM {
	byte_t* eeprom;
	unsigned write_ops;
} EEPROM;

EEPROM* init_eeprom() {
	EEPROM* eeprom = (EEPROM*)malloc(sizeof(EEPROM));
	eeprom->eeprom = (byte_t*)malloc(sizeof(byte_t) * EEPROM_SIZE);
	eeprom->write_ops = 0;
	return eeprom;
}

void eepromFree(EEPROM* eeprom) {
	free(eeprom->eeprom);
	free(eeprom);
}

byte_t read_eeprom(memory_t* mem) {
	byte_t eearh = readByte(mem, EEARH);
	byte_t eearl = readByte(mem, EEARL);
	addr_t addr = eearh << 8 | eearl;
	return mem->eeprom->eeprom[addr];
}

void write_eeprom(memory_t* mem) {
	byte_t eecr = readByte(mem, EECR);
	if(eecr & 1 << EEMPE && eecr & 1 << EEPE) {
		addr_t eear = readWord(mem, EEARL);
		byte_t eedr = readByte(mem, EEDR);
		mem->eeprom->eeprom[eear] = eedr;
		mem->eeprom->write_ops++;
		eecr &= ~(1 << EEPE);
		writeByte(mem, EECR, eecr);
	}
}