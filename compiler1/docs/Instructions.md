# Supported Instructions

|Instruction|Meaning|Tested|
|:---:|:---:|:---:|
|[ADC](#ADC)| Add with Carry | [x] |
|[ADD](#ADD)| Add without Carry|[x]|
|AND| Logical AND | [x] |
|ASR| Arithmetic Shift Right | [x] |
|BR| Branch on condition |[x]|
|COM| One's Complement | [x] |
|EOR| Exclusive logical OR | [x] |
|LSL| Logical left Shift | [x] |
|LSR| Logical right Shift | [x] |
|MOV| Move a value |[x]|
|MUL| Multiply Unsigned |[x]|
|MULS| Multiply Signed |[x]|
|MULSU| Multiply Signed with Unsigned |[x]|
|NEG| Two's Complement | [x] |
|OR| Logical OR |[x]|
|PUSH| PUSH on Stack |[x]|
|POP| POP on Stack |[x]|
|SBC| Subtract with Carry |[x]|
|SUB| Subtract without Carry |[x]|

## Syntax

This Compiler supports relativ flexible Syntax and provide a level of abstraktion compared to the pure Instructions.
*Importend* is the following Syntax:

```
{label:}
    <operation>{cond}{flag} <Rd>{,} {Rn}{,} {Operand2}{;}  {// Comment}
    <operation>{cond}{flag} <Rd>{,} {Rn}{,} {Operand2}{;}  {// Comment}
    <operation>{cond}{flag} <Rd>{,} {Rn}{,} {Operand2}{;}  {// Comment}
```

`<>` - needed
`{}` - optional

- <operation>: three letter opcode mnemonic, e.g. `MOV` or `ADD` (exception `BR`)
- {cond}: two letter condition code, e.g. `EQ` or `CS`
- {flag}: one letter optional flag, e.g. `S`
- <Rd>: destination register, e.g. `r1`
- {Rn}: first source Register or Immediate, e.g. `r12`or `#42`
- {Operand2}: a flexible second operand

### Register Pointer


## Instructions

Nomenclature:
|`rd` | destination Register |
|`rr` | source Register |
|`r:` | [Register Pointer](#Register-Pointer)|

### ADC

The `ADC` Instruction combines two AVG Instruction together. `ADC` allows to Add a value of a Register or directly an Immediate with Carry together.
This results to the following Syntax:
- `ADC rd rr`
- `ADC rd immediate`

The `immediate` can only be of size 8 bit, which leads to the range of 0-255.

### ADD

The `ADD` Instructions combines multiple AVG Instruction together. Compared to the `ADC` it ignores the Carry Bit.
`ADD` can add a Register or an Immediate to a register like `ADC` and even a Word from a [Register Pointer](#Register-Pointer).

- `ADD rd rr`
- `ADD rd immediate`
- `ADD rd r:`