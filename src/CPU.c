#include "CPU.h"

typedef struct AVR_CPU {
	addr_t SP;
	addr_t PC; // originally only 14 bits;
	gpr_t* gpr;
	memory_t* mem;
	sr_t* sr;
} cpu_t;

cpu_t* initCPU() {
	cpu_t* cpu = (cpu_t*)malloc(sizeof(cpu_t));
	cpu->SP = 0x08FF;
	cpu->PC = 0x0100;
	cpu->gpr = init_gpr();
	cpu->mem = init_memory(cpu->gpr);
	cpu->sr = init_sr();
	return cpu;
}

void flashMemory(cpu_t* cpu, addr_t addr, instruction_t inst) {
	writeWord(cpu->mem, addr, inst);
}

instruction_t fetch(cpu_t* cpu) {
	instruction_t instruction = readWord(cpu->mem, cpu->PC);
	cpu->PC += 2;
	return instruction;
}

void execute(cpu_t* cpu, CLOCK_CYCLE clockCycle) {
	while(clockCycle) {
		instruction_t instruction = fetch(cpu);
		operation_t op = getOperation(instruction);
		op(cpu, instruction);
		clockCycle--;
	}
}

byte_t readRegister(cpu_t* cpu, addr_t addr) {
	return gprReadByte(cpu->gpr, addr);
}

void writeRegister(cpu_t* cpu, addr_t addr, byte_t value) {
	gprWriteByte(cpu->gpr, addr, value);
}

word_t readMemory(cpu_t* cpu, addr_t addr) {
	return readWord(cpu->mem, addr);
}

sr_t* getSR(cpu_t* cpu) {
	return cpu->sr;
}

gpr_t* getGPR(cpu_t* cpu) {
	return cpu->gpr;
}

void addPC(cpu_t* cpu, byte_t steps) {
	cpu->PC += steps * 2;
}

void subPC(cpu_t* cpu, byte_t steps) {
	cpu->PC -= steps * 2;
}

void printGPRegister(cpu_t* cpu) {
	printRegister(cpu->gpr);
}

void freeCPU(cpu_t* cpu) {
	srFree(cpu->sr);
	memoryFree(cpu->mem);
	free(cpu);
}