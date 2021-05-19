
hi:
    ADD r0 r1 
    ADD r0 #1
    ADD r1 r2
jump:
    ADD r0 #1
    ADD r0 r1
    ADD r1 r2
    BRBC 1 hi


main:
    ADD r0 r1
    ADD r1 r2
    BRBC 1 jump
    ADD r0 r1 
    ADD r0 r1 
    ADD r0 r1 
    ADD r0 r1 
    ADD r0 r1 
    ADD r0 r1