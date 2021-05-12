#ifndef _REGISTER_H
#define _REGISTER_H

#include <stdio.h>
#include <stdlib.h>

#include "Types.h"

#define GPR_SIZE 32

typedef struct GeneralPurposeRegister gpr_t;

typedef struct StatusRegister sr_t;

gpr_t* init_gpr();
sr_t* init_sr();

void gprFree(gpr_t* gpr);
void srFree(sr_t* sr);

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

void setIFlag(sr_t* sr, bit_t value);
bit_t getIFlag(sr_t* sr);

void setTFlag(sr_t* sr, bit_t value);
bit_t getTFlag(sr_t* sr);

void setHFlag(sr_t* sr, bit_t value);
bit_t getHFlag(sr_t* sr);

void setSFlag(sr_t* sr, bit_t value);
bit_t getSFlag(sr_t* sr);

void setVFlag(sr_t* sr, bit_t value);
bit_t getVFlag(sr_t* sr);

void setNFlag(sr_t* sr, bit_t value);
bit_t getNFlag(sr_t* sr);

void setZFlag(sr_t* sr, bit_t value);
bit_t getZFlag(sr_t* sr);

void setCFlag(sr_t* sr, bit_t value);
bit_t getCFlag(sr_t* sr);

bit_t getFlag(sr_t* sr, byte_t addr);

#endif //_REGISTER_H