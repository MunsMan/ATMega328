# Goal of Today

Continue working on our own compiler, two compile `ARM` to `Machine Code`.
We started to write the compiler last time in `python` and will continue so.

- Finishing `BR`

New Instructions:

- ADC: rb = rb + rr + 1     Addition with Carry
- SUB: rb = rb - rr         Subtraction
- SBC: rb = rb - rr + c -1  Subtraction with Carray
- RSB: rb = rr - rb         reverse subtraction
- RSB: rb = rr - rb + c -1  reverse subtraction with Carry
- MUL:<needs some planning> multiplication