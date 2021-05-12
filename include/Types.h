#ifndef _TYPES_H
#define _TYPES_H

#include <stdint.h>
#include <stdlib.h>

#define INSTRUCTION_LENGTH 16
#define UNUSED(x) (void)(x)

typedef uint8_t byte_t;
typedef uint16_t word_t;
typedef byte_t GPR_ADDR;
typedef uint8_t bit_t;
typedef uint16_t addr_t;
typedef uint16_t instruction_t;

typedef uint64_t CLOCK_CYCLE;

typedef struct AVR_CPU cpu_t;

#endif // _TYPES_H