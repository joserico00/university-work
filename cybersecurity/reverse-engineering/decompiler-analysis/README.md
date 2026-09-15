# Ghidra Decompilation Analysis

An academic reverse-engineering presentation comparing original C source, disassembly, Ghidra's inferred pseudocode, and manually corrected decompilation.

The 32-slide presentation studies three examples from exercises based on *The C Programming Language*:

- a power function, where inferred parameter and return types differ from the source
- a quicksort implementation, where arrays and loop structure become harder to recognize
- an expression parser, where global state and reconstructed control flow complicate the output

## Files

- `Ghidra-Decompilation-Analysis.pptx` is the editable Spanish-language presentation.
- `Ghidra-Decompilation-Analysis.pdf` is the browser-friendly export.

## Main observations

Decompiled code is an approximation rather than recovered source. Type information, variable names, array boundaries, and high-level loop structure may disappear during compilation. A useful review compares the pseudocode with the disassembly, checks calling conventions and data widths, and renames variables only when the evidence supports the interpretation.

## Source material

The analyzed C exercises were drawn from [Heatwave/The-C-Programming-Language-2nd-Edition](https://github.com/Heatwave/The-C-Programming-Language-2nd-Edition), as cited in the presentation. This repository includes the analysis deck, not a copy of that upstream source tree.

## Language

The presentation is in Spanish. This README provides an English summary for recruiters and other GitHub visitors.

## Author

Jose E. Rodriguez Rios
