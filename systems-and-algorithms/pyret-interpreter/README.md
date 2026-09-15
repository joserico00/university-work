# Pyret Expression Interpreter

A small interpreter written in Pyret for programming-languages coursework. It separates a surface language from a smaller core language, then evaluates the core abstract syntax tree using lexical environments and closures.

## Implemented concepts

- S-expression parsing for numbers, booleans, arithmetic, equality, and conditional expressions
- Desugaring subtraction into addition and multiplication
- Separate surface and core abstract syntax trees
- Typed runtime values for numbers, booleans, and closures
- Lexical environment lookup
- Multi-argument functions with arity checks
- Automated examples with Pyret `check` blocks

The parser currently handles arithmetic and conditional source strings. Function definitions and applications are constructed directly with the core AST; extending the surface parser for function syntax is a natural next step.

## Run

1. Open [code.pyret.org](https://code.pyret.org/).
2. Create a program using the `essentials2021` context.
3. Paste or import `interpreter.arr`.
4. Select **Run**. The `check` block exercises parsing, desugaring, arithmetic, conditionals, equality, closures, and multi-argument application.

Example surface-language expressions:

```text
(+ 23 (* 5 6))
(- 10 3)
(== 4 4)
(if (== 2 3) 10 20)
```

## Origin

This version consolidates several code.pyret.org coursework drafts into one documented implementation. Duplicate and incomplete drafts were not included.

## Author

Jose E. Rodriguez Rios
