
MOV r16 #32
MOV r17 #224
ADD r16 r17 // r16 = 0 -> Z = 1
MOV r18 #1
BRBC 1 1 // NO JUMP
MOV r18 #10

MOV r19 #1
BRBC 2 1
MOV r19 #10




// FLAGS 
// C Z N
// 1 1 0 - - - - -

// SET = 1
// NO SET = 0