
hi:
    ADD r0 r1 
    ADD R0 #1
    ADD r1 r2
jump:
    ADD r0 #1
    ADD r0 r1
    ADD r1 r2
    BRBC 1, hi; // test
add1:
    ADD r0 1;

main:
    ASR r5
    ASR r5,5
    MOV r0      #8
    MOV r1 #1
    MOV r4 #2;
    AND r2 r0
    BREQ jump
    ADD X 63
    SUB Y 63
    SUB r0 r1
    ADD Z 63
    ADDNE r24:r25 63
    ADD r24: 63
    PUSH {r0 - r12, r16}
    POP {r0-r12, r16}
    MOV r13 r0

func:
    ADD r1, r2
    MOV r0, r1