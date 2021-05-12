#include "Register.h"

typedef struct GeneralPurposeRegister {
	byte_t* r;
	byte_t size;
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
} sr_t;

gpr_t* init_gpr() {
	gpr_t* gpr = (gpr_t*)malloc(sizeof(gpr_t));
	gpr->size = GPR_SIZE;
	gpr->r = (byte_t*)malloc(sizeof(byte_t) * gpr->size);
	gpr->X = 0x1A;
	gpr->Y = 0x1C;
	gpr->Z = 0x1E;
	return gpr;
}

sr_t* init_sr() {
	sr_t* sr = (sr_t*)malloc(sizeof(sr_t));
	sr->I = 0;
	sr->T = 0;
	sr->H = 0;
	sr->S = 0;
	sr->V = 0;
	sr->N = 0;
	sr->Z = 0;
	sr->C = 0;
	return sr;
}

void gprFree(gpr_t* gpr) {
	free(gpr->r);
	free(gpr);
}

void srFree(sr_t* sr) {
	free(sr);
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

void setIFlag(sr_t* sr, bit_t value) {
	sr->I = value;
}
bit_t getIFlag(sr_t* sr) {
	return sr->I;
}

void setTFlag(sr_t* sr, bit_t value) {
	sr->T = value;
}
bit_t getTFlag(sr_t* sr) {
	return sr->T;
}

void setHFlag(sr_t* sr, bit_t value) {
	sr->H = value;
}
bit_t getHFlag(sr_t* sr) {
	return sr->H;
}

void setSFlag(sr_t* sr, bit_t value) {
	sr->S = value;
}
bit_t getSFlag(sr_t* sr) {
	return sr->S;
}

void setVFlag(sr_t* sr, bit_t value) {
	sr->V = value;
}
bit_t getVFlag(sr_t* sr) {
	return sr->V;
}

void setNFlag(sr_t* sr, bit_t value) {
	sr->N = value;
}
bit_t getNFlag(sr_t* sr) {
	return sr->N;
}

void setZFlag(sr_t* sr, bit_t value) {
	sr->Z = value;
}
bit_t getZFlag(sr_t* sr) {
	return sr->Z;
}

void setCFlag(sr_t* sr, bit_t value) {
	sr->C = value;
}
bit_t getCFlag(sr_t* sr) {
	return sr->C;
}

bit_t getFlag(sr_t* sr, byte_t addr) {
	if(addr > 7) {
		fprintf(stderr, "Address out of scope!\n");
		exit(EXIT_FAILURE);
	}
	switch(addr) {
		case 0x0: {
			return getCFlag(sr);
		};
		case 0x1: {
			return getZFlag(sr);
		};
		case 0x2: {
			return getNFlag(sr);
		};
		case 0x3: {
			return getVFlag(sr);
		};
		case 0x4: {
			return getSFlag(sr);
		};
		case 0x5: {
			return getHFlag(sr);
		};
		case 0x6: {
			return getTFlag(sr);
		};
		case 0x7: {
			return getIFlag(sr);
		};
		default: return 0;
	}
	return 0;
}

void resetSR(sr_t* sr) {
	sr->I = 0;
	sr->T = 0;
	sr->H = 0;
	sr->S = 0;
	sr->V = 0;
	sr->N = 0;
	sr->Z = 0;
	sr->C = 0;
}