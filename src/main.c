#include <stdio.h>

#include "CPU.h"

typedef struct Instructions {
	instruction_t* instructions;
	unsigned nInstructions;
} instructions_t;

int testRegister();
int testMemory();
void test(char* name, int result);
instructions_t* readCode(char* file);
instruction_t sByteInt(char* byte, unsigned size);

int main(int argc, char* argv[]) {

	if(argc != 2) {
		fprintf(stderr, "Please provide the Instructions!\n");
		return EXIT_FAILURE;
	}
	cpu_t* cpu = initCPU();
	instructions_t* instructions = readCode(argv[1]);
	printf("%d Instructions loaded\n", instructions->nInstructions);

	addr_t pc = 0x0100;
	for(addr_t i = 0; i < (addr_t)instructions->nInstructions; i++) {
		flashMemory(cpu, pc + (i * 2), instructions->instructions[i]);
		printf("%d. 0x%02X = [0x%02X]\n", i, pc + (i * 2), readMemory(cpu, pc + (i * 2)));
	}
	execute(cpu, 100);
	printGPRegister(cpu);
}

instruction_t sByteInt(char* byte, unsigned size) {
	int res = 0x00;
	for(unsigned i = 0; i < size; i++) {
		if(byte[i] == '1') {
			res += 1 << (15 - i);
		}
	}
	return res;
}

instructions_t* readCode(char* file) {
	char* rawInst = (char*)malloc(sizeof(char) * INSTRUCTION_LENGTH);
	FILE* fp = fopen(file, "r");
	int nInst = 0;
	while(fgets(rawInst, INSTRUCTION_LENGTH + 1, fp)) {
		nInst++;
	}
	fclose(fp);

	instructions_t* instructions = (instructions_t*)malloc(sizeof(instructions_t));
	instructions->nInstructions = nInst;
	instructions->instructions = (instruction_t*)malloc(sizeof(instruction_t) * nInst);

	fp = fopen(file, "r");
	for(int i = 0; i < nInst; i++) {
		fgets(rawInst, INSTRUCTION_LENGTH + 1, fp);
		instructions->instructions[i] = sByteInt(rawInst, INSTRUCTION_LENGTH);
	}
	return instructions;
}

void test(char* name, int result) {
	if(result) {
		printf("Test completed: %s - success\n", name);
	} else {
		printf("Test failed: %s - fail\n", name);
		exit(EXIT_FAILURE);
	}
}

int testRegister() {
	gpr_t* gpr = init_gpr();
	word_t x = 0xFF11;
	word_t y = 0x0F11;
	word_t z = 0xFEFE;
	gprWriteX(gpr, x);
	gprWriteY(gpr, y);
	gprWriteZ(gpr, z);
	if(x != gprReadX(gpr)) {
		free(gpr);
		return 0;
	}
	if(y != gprReadY(gpr)) {
		free(gpr);
		return 0;
	}
	if(z != gprReadZ(gpr)) {
		free(gpr);
		return 0;
	}
	free(gpr);
	return 1;
}

int testMemory() {
	gpr_t* gpr = init_gpr();
	memory_t* mem = init_memory(gpr);
	writeByte(mem, 0x02F, 0x80);
	writeByte(mem, 0x030, 0xFF);
	word_t w1 = readWord(mem, 0x2F);
	writeWord(mem, 0x31, 0xFF80);
	word_t w2 = readWord(mem, 0x31);
	free(gpr);
	free(mem);
	return w1 == w2 && 0xFF80 == w2;
}

int testAdd() {
	cpu_t* cpu = initCPU();
	flashMemory(cpu, 0x0100, 0xC01);
	return 1;
}