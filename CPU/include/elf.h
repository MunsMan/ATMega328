#ifndef _ELF_H_
#define _ELF_H_

#include <stdlib.h>
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdbool.h>
#include <stdint.h>

#define ELF_HEADER_SIZE 64

typedef struct elf elf_t;

elf_t* readELF(int fd);

#endif  //_ELF_H_