#include "elf.h"

typedef struct elf {
    bool bit32;
    bool le;
    unsigned machine;
    unsigned start_section_header_table;
    unsigned size_section_header;
    unsigned num_section_header;
} elf_t;

typedef struct section {
    int offset;
    int size;
    int flag;
    int addr;
} section_t;

typedef struct section_table {
    int entries;
    section_t** sections;
} section_table_t;

int main(){
    char* file = readFile("test.elf");
    elf_t* elf = readELFHeader(file);
    printf("ELF:\n32 Bit: %d\nMachine Code: %u\nSection Header Start: %u\n Section Header Size: %u\nSection Header Number: %u\n", 
    elf->bit32, 
    elf->machine, 
    elf->start_section_header_table,
    elf->size_section_header,
    elf->num_section_header);
    section_table_t* section_table = readSections(file, elf);
    for(int i = 0; i < section_table->entries; i++){
        section_t* section = section_table->sections[i];
        printf("ADDR: %u\t OFFSET: %u\t SIZE: %u\t FLAGS: %u\n", section->addr, section->offset, section->size, section->flag);
    }
    return EXIT_SUCCESS;    
}

char* readFile(char* filename){
    FILE* fd = fopen(filename, "rb");
    fseek(fd, 0, SEEK_END);
    size_t fsize = ftell(fd);
    fseek(fd, 0, SEEK_SET);

    char* file = malloc(fsize +1);
    fread(file, 1, fsize, fd);
    fclose(fd);
    file[fsize] = 0;
    return file;
}

elf_t* readELFHeader(char* file){    
    elf_t* elf = malloc(sizeof(elf_t));
    elf->bit32 = file[0x04] == 1 ? true : false;
    elf->le = file[0x5] == 1 ? true : false;
    elf->machine = (uint16_t)(file[0x12]);
    if(elf->bit32){
        elf->start_section_header_table = littleEndiness32((uint32_t)file[0x20]);
        elf->size_section_header = (uint16_t)file[0x2E];
        elf->num_section_header = (uint16_t)file[0x30];
    }
    return elf;
}

section_table_t* readSections(char* file, elf_t* elf){
    section_table_t* table = malloc(sizeof(section_table_t));
    section_t** sections = (section_t**)malloc(sizeof(section_t*) *elf->num_section_header);
    table->entries = elf->num_section_header;
    table->sections = sections;
    for(int i = 0; i < table->entries; i++){
        table->sections[i] = readSectionHeader(&file[elf->start_section_header_table + elf->size_section_header * i]);
    }
    return table;
};

void destroy_section_table(section_table_t* section_table){
    for(int i = 0; i < section_table->entries; i++){
        free(section_table->sections[i]);
    }
    free(section_table);
}

section_t* readSectionHeader(char* header){
    section_t* section = malloc(sizeof(section_t));
    section->flag = (uint32_t)header[0x08];
    section->offset = (uint32_t)header[0x10];
    section->size = (uint32_t)header[0x14];
    section->addr = (uint32_t)header[0x0C];
    return section;
}

unsigned littleEndiness32(unsigned num){
    return 
    ((num & 0x000000FF) << 24) |
    ((num & 0x0000FF00) << 8) |
    ((num & 0x00FF0000) >> 8) |
    ((num & 0xFF000000) >> 24);
}