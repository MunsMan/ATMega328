#include "types.h"
#include "cpu.h"
#include "board.h"

int main(){

    // INIT - CPU
    memory_t* memory = init_memory();
    cpu_t* cpu = init_cpu(memory);

    // FLASH
    write_flash(cpu->memory, 0x0000, 3073);


    printf("Zero Flag: %d\n", getZ(cpu));
    // Execute
    int clock_cycle = execute(cpu);

    printf("The first operation took %d cycles.\n", clock_cycle);
    printf("Zero Flag: %d\n", getZ(cpu));

    // DESTROY - CPU
    destroy_cpu(cpu);

    return EXIT_SUCCESS;
}