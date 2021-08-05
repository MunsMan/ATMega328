#include "avr_memory.h"

typedef struct memory {
    size_t sram_size;
    size_t flash_size;
    byte_t* sram;    
    instruction_t* flash;
} memory_t;

memory_t* init_memory(){
    memory_t* memory = (memory_t*)malloc(sizeof(memory_t));
    memory->sram = (byte_t*)malloc(sizeof(byte_t) * SIZE_SRAM);
    memory->flash = (instruction_t*)malloc(sizeof(word_t) * SIZE_FLASH);
    memory->sram_size = SIZE_SRAM;
    memory->flash_size = SIZE_FLASH;
    return memory;
}

bool destroy_memory(memory_t* memory) {
    if(!(memory && (memory->sram || memory->flash))) return false;
    free(memory->sram);
    free(memory->flash);
    free(memory);
    return true;
}

byte_t read_sram(memory_t* memory, addr_t addr){
    return memory->sram[addr];
}

instruction_t read_flash(memory_t* memory, addr_t addr){
    return memory->flash[addr];
}

void write_sram(memory_t* memory, addr_t addr, byte_t byte){
    memory->sram[addr] = byte;
}

void write_flash(memory_t* memory, addr_t addr, instruction_t word){
    memory->flash[addr] = word;
}

bool check_addr_sram(memory_t* memory, addr_t addr){
    if(addr < memory->sram_size) return true;
    return false;
}

bool check_addr_flash(memory_t* memory, addr_t addr){
    if(addr < memory->flash_size) return true;
    return false;
}

void erase_memory(memory_t* memory){
    for(unsigned int i = 0; i < memory->sram_size; i ++){
        memory->sram[i] = 0;
    }
    for(unsigned int i = 0; i < memory->flash_size; i ++){
        memory->flash[i] = 0;
    }
}

void flash_loadable(char* file, memory_t* memory, loadable_t* loadable){
    for(unsigned i = 0; i < loadable->size / 2; i++){
        instruction_t instruction = ((instruction_t*)&file[loadable->offset])[i];
        write_flash(memory, loadable->addr + i, instruction);
    } 
}

void flash_memory(memory_t* memory, char* filename){
    char* file = readFile(filename);
    load_table_t* load_table = parseElf(file);
    for(int i = 0; i < load_table->num_sections; i++){
        flash_loadable(file, memory, load_table->loadables[i]);
    }
    destroy_load_table(load_table);
    free(file);
}

void dump_flash(memory_t* memory, int fd){
    write(fd, memory->flash, memory->flash_size);
}

void memory_dump(memory_t* memory){
    int fd = open("memory_dump.txt", O_CREAT | O_WRONLY);
    dump_flash(memory, fd);
}

size_t sram_size(memory_t* memory){
    return memory->sram_size;
}

size_t flash_size(memory_t* memory){
    return memory->flash_size;
}