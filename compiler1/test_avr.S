RESET:
    rjmp INIT

INIT:
    ldi r16, 10;
    ldi r17, 20;
    mov r0, r16;
    mov r1, r17;
TASK:
    add r0, r1;
