#ifndef _REGISTER_H
#define _REGISTER_H

#include <stdio.h>
#include <stdlib.h>

#include "Types.h"

#define GPR_SIZE 32

typedef struct GeneralPurposeRegister gpr_t;

typedef struct StatusRegister sreg_t;

gpr_t* init_gpr();
sreg_t* init_sr();

void gprFree(gpr_t* gpr);
void srFree(sreg_t* sreg);

byte_t gprReadByte(gpr_t* gpr, GPR_ADDR addr);
word_t gprReadWord(gpr_t* gpr, GPR_ADDR addr);
word_t gprReadX(gpr_t* gpr);
word_t gprReadY(gpr_t* gpr);
word_t gprReadZ(gpr_t* gpr);
void gprWriteByte(gpr_t* gpr, GPR_ADDR addr, byte_t value);
void gprWriteWord(gpr_t* gpr, GPR_ADDR addr, word_t value);
void gprWriteX(gpr_t* gpr, word_t value);
void gprWriteY(gpr_t* gpr, word_t value);
void gprWriteZ(gpr_t* gpr, word_t value);

void printRegister(gpr_t* gpr);

void setIFlag(sreg_t* sreg, bit_t value);
bit_t getIFlag(sreg_t* sreg);

void setTFlag(sreg_t* sreg, bit_t value);
bit_t getTFlag(sreg_t* sreg);

void setHFlag(sreg_t* sreg, bit_t value);
bit_t getHFlag(sreg_t* sreg);

void setSFlag(sreg_t* sreg, bit_t value);
bit_t getSFlag(sreg_t* sreg);

void setVFlag(sreg_t* sreg, bit_t value);
bit_t getVFlag(sreg_t* sreg);

void setNFlag(sreg_t* sreg, bit_t value);
bit_t getNFlag(sreg_t* sreg);

void setZFlag(sreg_t* sreg, bit_t value);
bit_t getZFlag(sreg_t* sreg);

void setCFlag(sreg_t* sreg, bit_t value);
bit_t getCFlag(sreg_t* sreg);

bit_t getFlag(sreg_t* sreg, byte_t addr);

#endif //_REGISTER_H