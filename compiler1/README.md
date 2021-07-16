# Compiler

This is a Compiler which compiles ARMisch Code into AVG Assembly or rather in AVG Bitcode.

The goal is to provide an easier writing experience to the programming. This layer of abstractions comes with the cost of a bit performance. There are some instructions, with are not directly supported and compile to multiple Instructions under the hut.

## Instructions
The Instructions, which are supported and the correstponding Syntax if defined in the Documentaion. Please always reference to the documentation and open a Issue if something is missing or incorrect.

[Documentation](https://github.com/MunsMan/ATMega328/tree/Compiler/compiler1/docs)

## Performance
An important topic, when working that low level. The goal is to map Instructions as direct as possible. But for further improvements, the goal is, to reduce the amount of instructions and clock cycles. In the documentation, it is pointed out, which instructions are efficient and which should be avoided in time critical use cases.

## Error Handling
To further enhances the User Experience, the compiler provides its own Error Message Library. Error are usually throw with the corresponding Line Number and the contest. Then there is a custom Message appended, which provides further information. This should lead to faster debugging and a better understanding of the language.

## Testing
To ensure that the compiler works, it contains a wide range of tests and we are working on expanding this arsenal continually. To avoid disasters, the goal is to follow the principles of [TDD](https://en.wikipedia.org/wiki/Test-driven_development)


## Get Started

Write your one assembly file. Because we are trying to be as close to the ARM Syntax, you should be good writing that.

Then just compile your code using:

`./main.py <you-file>`

And you are good to go.

If you have problems, always reference to our documentation firs: [DOCS](https://github.com/MunsMan/ATMega328/tree/Compiler/compiler1/docs)
