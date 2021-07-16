# Supported Instructions

|Instruction|Meaning|Tested|
|:---:|:---:|:---:|
|ADC| Add with Carry | [x] |
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

## Instructions

### ADD

The `ADD` allows the addition of two Registers. This Addition ignores the Carry Bit.
The `ADD` supports different Syntax.

- `ADD` `<Register>` `<Register>`
- `ADD` `<Register>` `<Immediate>`
