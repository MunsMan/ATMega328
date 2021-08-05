#ifndef _ELF_H_
#define _ELF_H_

#include <stdlib.h>
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdbool.h>
#include <stdint.h>

#define ELF_HEADER_SIZE 64

typedef struct loadable {
    unsigned offset;
    unsigned size;
    unsigned addr;
} loadable_t;

typedef struct load_table {
    int num_sections;
    loadable_t** loadables;
} load_table_t;

typedef struct section_table section_table_t;
typedef struct section section_t;
typedef struct elf elf_t;

elf_t* readELFHeader(char* filename);
char* readFile(char* file);

load_table_t* parseElf(char* file);

loadable_t* getLoadable(section_t* section);

section_table_t* readSections(char* file, elf_t* elf);
section_t* readSectionHeader(char* header);
void destroy_section_table(section_table_t* section_table);
void destroy_load_table(load_table_t* load_table);

unsigned bigEndianess(char* start, int length);
bool shouldLoad(section_t* section);


#endif  //_ELF_H_