#include "include/memory.h"

typedef struct memory {
    size_t sram_size;
    size_t flash_size;
    byte_t* sram;    
    instruction_t* flash;
} memory_t;

memory_t* init_memory(){
    memory_t* memory = (memory_t*)malloc(sizeof(memory_t));
    memory->sram = (byte_t*)malloc(sizeof(byte_t) * SIZE_SRAM);
    memory->flash = (word_t*)malloc(sizeof(word_t) * SIZE_FLASH);
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

// ToDo: Need implementation
bool flash_memory(memory_t* memory, char* filename);

size_t sram_size(memory_t* memory){
    return memory->sram_size;
}

size_t flash_size(memory_t* memory){
    return memory->flash_size;
}