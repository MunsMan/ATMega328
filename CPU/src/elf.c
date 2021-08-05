#include "elf.h"

typedef struct elf {
    bool bit32;
    bool le;
    unsigned machine;
    unsigned byte1;
    unsigned byte2;
    unsigned byte3;
    unsigned byte4;
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

char* readFile(char* filename){
    FILE* fd = fopen(filename, "rb");
    if(!fd){
        fprintf(stderr, "Unable to load file!\n");
        exit(EXIT_FAILURE);
    }
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
        elf->byte1 = ((uint8_t*)file)[0x20];
        elf->byte2 = file[0x21];
        elf->byte3 = file[0x22];
        elf->byte4 = file[0x23];
        elf->start_section_header_table = bigEndianess(&file[0x20], 4);
        elf->size_section_header = (uint16_t)file[0x2E];
        elf->num_section_header = (uint16_t)file[0x30];
    }
    return elf;
}

load_table_t* parseElf(char* file){
    elf_t* elf = readELFHeader(file); 
    section_table_t* section_table = readSections(file, elf);
    load_table_t* load_table = malloc(sizeof(load_table_t));
    load_table->num_sections = 0;
    load_table->loadables = (loadable_t**)malloc(sizeof(loadable_t*) * section_table->entries);
    for(int i = 0; i < section_table->entries;i++){
        if(shouldLoad(section_table->sections[i])){
            loadable_t* loadable = getLoadable(section_table->sections[i]);

            load_table->loadables[load_table->num_sections++]  = loadable;
        }
    }
    destroy_section_table(section_table);
    return load_table;
}

loadable_t* getLoadable(section_t* section){
    loadable_t* loadable = malloc(sizeof(loadable_t));
    loadable->offset = section->offset;
    loadable->size = section->size;
    loadable->addr = section->addr;
    return loadable;
}

section_table_t* readSections(char* file, elf_t* elf){
    section_table_t* table = malloc(sizeof(section_table_t));
    table->sections = (section_t**)malloc(sizeof(section_t*) *elf->num_section_header);
    table->entries = elf->num_section_header;
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

void destroy_load_table(load_table_t* load_table){
    for(int i = 0; i < load_table->num_sections; i++){
        free(load_table->loadables[i]);
    }
    free(load_table->loadables);
    free(load_table);
}

section_t* readSectionHeader(char* header){
    section_t* section = malloc(sizeof(section_t));
    section->flag = bigEndianess(&header[0x08], 4);
    section->offset = bigEndianess(&header[0x10], 4);
    section->size = bigEndianess(&header[0x14], 4);
    section->addr = bigEndianess(&header[0x0C], 4);
    return section;
}

unsigned bigEndianess(char* start, int length){
    unsigned res = 0;
    for(int i = 0; i < length; i++){
        res += ((uint8_t*)start)[i] << (8 * i);
    }
    return res;
}

bool shouldLoad(section_t* section){
    if(section->flag & 0x7) return true;
    return false;
}