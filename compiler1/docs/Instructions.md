# Supported Instructions

|Instruction|Meaning|example|Tested|
|:---:|:---:|:---:|:---:|
|ADD| Adding register or constants together| ADD r1 #5 |[x]|
|AND| Logical AND | AND r1 r2 | [ ] |
|MOV| Move Register or Constants to another Register | MOV r5 #45 |[x]|

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