#include "Register.h"

typedef struct GeneralPurposeRegister {
	byte_t* r;
	byte_t size;
	// FixMe: Change to Pointer	
	GPR_ADDR X;
	GPR_ADDR Y;
	GPR_ADDR Z;
} gpr_t;

typedef struct StatusRegister {
	bit_t I : 1; // Global Interrupt Enable
	bit_t T : 1; // Bit Copy Storage
	bit_t H : 1; // Half Carry Flag
	bit_t S : 1; // Sign Bit
	bit_t V : 1; // Two's Complement Overflow Flag
	bit_t N : 1; // Negative Flag
	bit_t Z : 1; // Zero Flag
	bit_t C : 1; // Carry Flag
} sreg_t;

gpr_t* init_gpr() {
	gpr_t* gpr = (gpr_t*)malloc(sizeof(gpr_t));
	gpr->size = GPR_SIZE;
	gpr->r = (byte_t*)malloc(sizeof(byte_t) * gpr->size);
	gpr->X = 0x1A;
	gpr->Y = 0x1C;
	gpr->Z = 0x1E;
	return gpr;
}

sreg_t* init_sr() {
	sreg_t* sreg = (sreg_t*)malloc(sizeof(sreg_t));
	sreg->I = 0;
	sreg->T = 0;
	sreg->H = 0;
	sreg->S = 0;
	sreg->V = 0;
	sreg->N = 0;
	sreg->Z = 0;
	sreg->C = 0;
	return sreg;
}

void gprFree(gpr_t* gpr) {
	free(gpr->r);
	free(gpr);
}

void srFree(sreg_t* sreg) {
	free(sreg);
}

byte_t gprReadByte(gpr_t* gpr, GPR_ADDR addr) {
	return gpr->r[addr % 0x20];
}

word_t gprReadWord(gpr_t* gpr, GPR_ADDR addr) {
	return (word_t)gpr->r[addr + 1] << 8 | gpr->r[addr];
}

word_t gprReadX(gpr_t* gpr) {
	return gprReadWord(gpr, gpr->X);
}

word_t gprReadY(gpr_t* gpr) {
	return gprReadWord(gpr, gpr->Y);
}
word_t gprReadZ(gpr_t* gpr) {
	return gprReadWord(gpr, gpr->Z);
}

void gprWriteByte(gpr_t* gpr, GPR_ADDR addr, byte_t value) {
	gpr->r[addr] = value;
}
void gprWriteWord(gpr_t* gpr, GPR_ADDR addr, word_t value) {
	byte_t first = (byte_t)value;
	byte_t sec = (word_t)value >> 8;
	gpr->r[addr] = first;
	gpr->r[addr + 1] = sec;
}

void gprWriteX(gpr_t* gpr, word_t value) {
	gprWriteWord(gpr, gpr->X, value);
}
void gprWriteY(gpr_t* gpr, word_t value) {
	gprWriteWord(gpr, gpr->Y, value);
}
void gprWriteZ(gpr_t* gpr, word_t value) {
	gprWriteWord(gpr, gpr->Z, value);
}

void printRegister(gpr_t* gpr) {
	for(unsigned i = 0; i < gpr->size; i++) {
		printf("[ R%d | 0x%02X ]\n", i, gprReadByte(gpr, i));
	}
}

void setIFlag(sreg_t* sreg, bit_t value) {
	sreg->I = value;
}
bit_t getIFlag(sreg_t* sreg) {
	return sreg->I;
}

void setTFlag(sreg_t* sreg, bit_t value) {
	sreg->T = value;
}
bit_t getTFlag(sreg_t* sreg) {
	return sreg->T;
}

void setHFlag(sreg_t* sreg, bit_t value) {
	sreg->H = value;
}
bit_t getHFlag(sreg_t* sreg) {
	return sreg->H;
}

void setSFlag(sreg_t* sreg, bit_t value) {
	sreg->S = value;
}
bit_t getSFlag(sreg_t* sreg) {
	return sreg->S;
}

void setVFlag(sreg_t* sreg, bit_t value) {
	sreg->V = value;
}
bit_t getVFlag(sreg_t* sreg) {
	return sreg->V;
}

void setNFlag(sreg_t* sreg, bit_t value) {
	sreg->N = value;
}
bit_t getNFlag(sreg_t* sreg) {
	return sreg->N;
}

void setZFlag(sreg_t* sreg, bit_t value) {
	sreg->Z = value;
}
bit_t getZFlag(sreg_t* sreg) {
	return sreg->Z;
}

void setCFlag(sreg_t* sreg, bit_t value) {
	sreg->C = value;
}
bit_t getCFlag(sreg_t* sreg) {
	return sreg->C;
}

bit_t getFlag(sreg_t* sreg, byte_t addr) {
	if(addr > 7) {
		fprintf(stderr, "Address out of scope!\n");
		exit(EXIT_FAILURE);
	}
	switch(addr) {
		case 0x0: {
			return getCFlag(sreg);
		};
		case 0x1: {
			return getZFlag(sreg);
		};
		case 0x2: {
			return getNFlag(sreg);
		};
		case 0x3: {
			return getVFlag(sreg);
		};
		case 0x4: {
			return getSFlag(sreg);
		};
		case 0x5: {
			return getHFlag(sreg);
		};
		case 0x6: {
			return getTFlag(sreg);
		};
		case 0x7: {
			return getIFlag(sreg);
		};
		default: return 0;
	}
	return 0;
}

void resetSR(sreg_t* sreg) {
	sreg->I = 0;
	sreg->T = 0;
	sreg->H = 0;
	sreg->S = 0;
	sreg->V = 0;
	sreg->N = 0;
	sreg->Z = 0;
	sreg->C = 0;
}