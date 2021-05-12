#include "ALU.h"

byte_t _add(sr_t* sr, byte_t rd, byte_t rr) {
	byte_t r = 0x00;
	bit_t c = getCFlag(sr);
	bit_t rdi;
	bit_t rri;
	bit_t ri;

	for(byte_t i = 0; i < 8; i++) {

		rdi = (rd & (1 << i)) >> i;
		rri = (rr & (1 << i)) >> i;

		ri = (rdi ^ rri) ^ c;
		c = (rdi & rri) | ((rdi ^ rri) & c);

		r += ri << i;

		if(i == 2) {
			setHFlag(sr, c);
		}
	}
	setVFlag(sr, (rd >> 7 & rr >> 7 & ~r >> 7) | (~rd >> 7 & ~rr >> 7 & r >> 7));
	setNFlag(sr, r >> 7);
	setSFlag(sr, getVFlag(sr) ^ getNFlag(sr));
	setZFlag(sr, r == 0x00);
	setCFlag(sr, c);
	return r;
}

void addByteFlags(sr_t* sr, byte_t res);

void addByteFlags(sr_t* sr, byte_t res) {
	setCFlag(sr, (bit_t)res >> 8);
	setZFlag(sr, res == 0x00);
	setNFlag(sr, res < 0x00);
	setHFlag(sr, (bit_t)res >> 8);
	setVFlag(sr, (bit_t)res >> 8);
}

void add(cpu_t* cpu, instruction_t instruction) {
	addr_t rd = getRd(instruction);
	addr_t rr = getRr(instruction);
	byte_t r1 = readRegister(cpu, rd);
	byte_t r2 = readRegister(cpu, rr);
	sr_t* sr = getSR(cpu);
	setCFlag(sr, 0);
	writeRegister(cpu, rd, _add(sr, r1, r2));
}

void adc(cpu_t* cpu, instruction_t instruction) {
	addr_t rd = getRd(instruction);
	addr_t rr = getRd(instruction);
	byte_t r1 = readRegister(cpu, rd);
	byte_t r2 = readRegister(cpu, rr);
	writeRegister(cpu, rd, _add(getSR(cpu), r1, r2));
}

void adiw(cpu_t* cpu, instruction_t instruction) {
	byte_t K = ((instruction >> 2) & 0x30) + (instruction & 0xF);
	byte_t reg = (instruction >> 4) & 0x3;
	gpr_t* gpr = getGPR(cpu);
	sr_t* sr = getSR(cpu);
	switch(reg) {
		case 0x1: {
			gprWriteX(gpr, _adiw(sr, gprReadX(gpr), K));
		} break;
		case 0x2: {
			gprWriteY(gpr, _adiw(sr, gprReadY(gpr), K));
		} break;
		case 0x3: {
			gprWriteZ(gpr, _adiw(sr, gprReadZ(gpr), K));
		} break;
		default: {
			fprintf(stderr, "ADIW Register Code not definde");
			nop(cpu, instruction);
		} break;
	}
}

void land(cpu_t* cpu, instruction_t instruction) {
	addr_t addrRd = getRd(instruction);
	addr_t addrRr = getRr(instruction);

	byte_t Rd = readRegister(cpu, addrRd);
	byte_t Rr = readRegister(cpu, addrRr);
	sr_t* sr = getSR(cpu);
	byte_t R = _and(sr, Rd, Rr);
	writeRegister(cpu, addrRd, R);
}

void andi(cpu_t* cpu, instruction_t instruction) {
	addr_t addrRd = instruction & 0xF0;
	byte_t k = ((instruction >> 4) & 0xF0) + (instruction & 0xF);
	byte_t Rd = readRegister(cpu, addrRd);
	sr_t* sr = getSR(cpu);
	byte_t R = _and(sr, Rd, k);
	writeRegister(cpu, addrRd, R);
}

byte_t _and(sr_t* sr, byte_t Rd, byte_t Rr) {
	byte_t R = Rd & Rr;
	bit_t R7 = R >> 7;
	setVFlag(sr, 0);
	setNFlag(sr, R7);
	setSFlag(sr, 0 ^ R7);
	setZFlag(sr, R == 0);
	return R;
}

void asr(cpu_t* cpu, instruction_t instruction) {
	addr_t addrRd = (instruction >> 4) & 0x1F;
	byte_t Rd = readRegister(cpu, addrRd);
	bit_t R7 = Rd & 0x8;
	bit_t Rd0 = Rd & 0x1;
	byte_t R = (Rd & 0x7F) >> 1;
	R += R7;
	writeRegister(cpu, addrRd, R);
	sr_t* sr = getSR(cpu);
	setSFlag(sr, (R7 ^ Rd0) ^ R7);
	setVFlag(sr, R7 ^ Rd0);
	setNFlag(sr, R7);
	setZFlag(sr, R == 0);
	setCFlag(sr, Rd0);
}

word_t _adiw(sr_t* sr, word_t Rd, byte_t k) {
	setCFlag(sr, 0);
	byte_t Rl = _add(sr, Rd & 0xFF, k);
	byte_t Rh = _add(sr, Rd >> 8, 0);
	word_t R = (Rh << 8) + Rl;
	bit_t Rdh7 = (Rd >> 15) & 1;
	bit_t R15 = (R >> 15) & 1;
	setVFlag(sr, ~Rdh7 & R15);
	setNFlag(sr, R15);
	setSFlag(sr, getNFlag(sr) ^ getVFlag(sr));
	setZFlag(sr, R == 0);
	setCFlag(sr, ~R15 & Rdh7);
	return R;
}

void bclr(cpu_t* cpu, instruction_t instruction) {
	byte_t s = (instruction >> 4) & 0x7;
	sr_t* sr = getSR(cpu);
	switch(s) {
		case 0x0: {
			setCFlag(sr, 0);
		};
		case 0x1: {
			setZFlag(sr, 0);
		};
		case 0x2: {
			setNFlag(sr, 0);
		};
		case 0x3: {
			setVFlag(sr, 0);
		};
		case 0x4: {
			setSFlag(sr, 0);
		};
		case 0x5: {
			setHFlag(sr, 0);
		};
		case 0x6: {
			setTFlag(sr, 0);
		};
		case 0x7: {
			setIFlag(sr, 0);
		};
		default: break;
	}
}

void bld(cpu_t* cpu, instruction_t instruction) {
	addr_t addrRd = getRd(instruction);
	byte_t Rd = readRegister(cpu, addrRd);
	byte_t b = instruction & 0x7;
	sr_t* sr = getSR(cpu);
	bit_t T = getTFlag(sr);
	Rd = T << b;
	writeRegister(cpu, addrRd, Rd);
}

void brbc(cpu_t* cpu, instruction_t instruction) {
	byte_t k = (instruction >> 3) & 0x7F;
	byte_t s = instruction & 0x7;
	bit_t flag = getFlag(getSR(cpu), s);

	if(!flag) {
		if(k >> 7) {
			subPC(cpu, k & 0x3F);
		} else {
			addPC(cpu, k & 0x3F);
		}
	}
}

// ToDo: Implement Flags
void sbiw(cpu_t* cpu, instruction_t instruction) {
	byte_t c = ((instruction >> 2) & 0x30) + (instruction & 0xF);
	byte_t reg = (instruction >> 4) & 0x3;
	gpr_t* gpr = getGPR(cpu);
	switch(reg) {
		case 0x1: {
			gprWriteX(gpr, gprReadX(gpr) - c);
		} break;
		case 0x2: {
			gprWriteY(gpr, gprReadY(gpr) - c);
		} break;
		case 0x3: {
			gprWriteZ(gpr, gprReadZ(gpr) - c);
		} break;
		default: {
			fprintf(stderr, "SBIW Register Code not definde");
			nop(cpu, instruction);
		} break;
	}
}