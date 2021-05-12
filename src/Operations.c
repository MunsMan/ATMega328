#include "Operations.h"

operation_t getOperation(instruction_t instruction) {
	if(instruction >> 14 == 0) {
		return twoOperation(instruction);
	}
	if(instruction >> 14 == 1) {
		return registerImmediate(instruction);
	}
	if(instruction >> 10 == 0x24) {
		return loadStore(instruction);
	}
	if((instruction >> 9 == 0x4A) && ((instruction >> 3) & 1) == 0) {
		return oneOperation(instruction);
	}
	if((instruction >> 8 == 0x95) && ((instruction & 0xF) == 0x8)) {
		return zeroOperation(instruction);
	}
	if((instruction >> 9) == 0x4b) {
		return ((instruction >> 8) & 1) == 0 ? adiw : sbiw;
	}
	if((instruction >> 12) == 0xE) {
		return ldi;
	}
	if((instruction >> 7) == 0x129 && (instruction & 0xF) == 0x8) {
		return bclr;
	}
	if((instruction >> 11) == 0x1E) {
		return conditionalBranch(instruction);
	}
	fprintf(stderr, "Operation not defined!\n");
	return nop;
}

operation_t twoOperation(instruction_t instruction) {
	byte_t opcode = instruction >> 10;
	switch(opcode) {
		case 0x3: {
			return add;
		} break;
		case 0x7: {
			return adc;
		} break;
		default: {
			return nop;
		} break;
	}
}

addr_t getRd(instruction_t instruction) {
	return (instruction >> 4) & 0x1F;
}

addr_t getRr(instruction_t instruction) {
	return (((instruction >> 9) & 1) << 4) + (instruction & 0xF);
}

operation_t basicOperation(instruction_t instruction) {
	fprintf(stderr, "Operation not defined! 0x%04X\n", instruction);
	return nop;
}

operation_t oneOperation(instruction_t instruction) {
	fprintf(stderr, "Operation not defined! 0x%04X\n", instruction);
	return NULL;
}
operation_t zeroOperation(instruction_t instruction) {
	fprintf(stderr, "Operation not defined! 0x%04X\n", instruction);
	return NULL;
}
operation_t registerImmediate(instruction_t instruction) {
	fprintf(stderr, "Operation not defined! 0x%04X\n", instruction);
	return NULL;
}
operation_t loadStore(instruction_t instruction) {
	fprintf(stderr, "Operation not defined! 0x%04X\n", instruction);
	return NULL;
}

operation_t conditionalBranch(instruction_t instruction) {
	if((instruction >> 0xA) & 1) {
		return brbc;
	} else {
		fprintf(stderr, "Operation not defined! 0x%04X\n", instruction);
		return nop;
	}
}

void nop(cpu_t* cpu, instruction_t instruction) {
	UNUSED(cpu);
	UNUSED(instruction);
}

void ldi(cpu_t* cpu, instruction_t instruction) {
	addr_t reg = ((instruction >> 4) & 0xF) + 16;
	byte_t var = ((instruction >> 4) & 0xF0) + (instruction & 0xF);
	writeRegister(cpu, reg, var);
}
