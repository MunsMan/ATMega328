
hi:
    ADD r1 r2;
    ADD r1 #5;

main:

    MOV r1 #4 // ldi r23 #4 -> MOV r1 r23 
    MOV r16 #32
    MOV r17 #224
    ADD r16 r17 // r16 = 0 -> Z = 1
    MOV r18 #1
    BRBC 1 jumpto // NO JUMP
    MOV r18 #10

    MOV r19 #1
    BRBC 2 1
    MOV r19 #10

jumpto:
    MOV r17 #31;

// [0x00] ldi 
// [0x01] ldi
// [0x02] add
// [0x03] ldi
// [0x04] brbc
// [0x05] ldi


// [0x0A] ldi

