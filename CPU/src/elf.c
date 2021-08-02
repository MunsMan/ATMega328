#include "elf.h"

typedef struct elf {
    bool bit32;
    int machine;
    int start_section_header_table;
    int size_section_header;
    int num_section_header;
} elf_t;

typedef struct section {
    int offset;
    int size;
    int flag;
    int addr;
} section_t;

int main(){
    int fd = open("test.elf", O_RDONLY);
    elf_t* elf = readELF(fd);
    printf("ELF:\n32 Bit: %d\nMachine Code: %d\nSection Header: %d\n", elf->bit32, elf->machine, elf->start_section_header);
    close(fd);
    return EXIT_SUCCESS;    
}


elf_t* readELF(int fd){    
    char header[ELF_HEADER_SIZE];
    int num_read = read(fd, &header, ELF_HEADER_SIZE);
    if(num_read != ELF_HEADER_SIZE){
        fprintf(stderr, "Couldn't read full header");
        exit(EXIT_FAILURE);
    }
    elf_t* elf = malloc(sizeof(elf_t));
    elf->bit32 = header[0x04] == 1 ? true : false;
    elf->machine = (uint16_t)(header[0x12]);
    if(elf->bit32){
        elf->start_section_header = (uint32_t)header[0x20];
        elf->size_section_header = (uint16_t)header[0x2E];
        elf->num_section_header = (uint16_t)header[0x30];
    }
    return elf;
}

section_t* readSectionHeader(char* header, elf_t* elf){
    section_t* section = malloc(sizeof(section_t));
    section->flag = (uint32_t)header[0x08];
    section->offset = (uint32_t)header[0x10];
    section->size = (uint32_t)header[0x14];
    section->addr = (uint32_t)header[0x0C];
    return section;
}