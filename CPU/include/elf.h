#ifndef _ELF_H_
#define _ELF_H_

#include <stdlib.h>
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdbool.h>
#include <stdint.h>

#define ELF_HEADER_SIZE 64

typedef struct section_table section_table_t;
typedef struct section section_t;
typedef struct elf elf_t;

elf_t* readELFHeader(char* filename);
char* readFile(char* file);

section_table_t* readSections(char* file, elf_t* elf);
section_t* readSectionHeader(char* header);
void destroy_section_table(section_table_t* section_table);

unsigned littleEndiness32(unsigned num);

#endif  //_ELF_H_