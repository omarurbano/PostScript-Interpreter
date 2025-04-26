# PostScript-Interpreter

## Overview

Postscript-Inerpreter uses python to mimic how postscript programming language operates. It demonstrates a perfect example of dynamic scoping and can toggle between dynamic and lexical scoping to see how it behaves. There are over 40 operations already impelmented. Go ahead and give it a try

## Features

- Dynamic Scoping
- Lexical Scoping
- Arthemtic operations
- Conditional operations
- Stack Manipulation
- Dictionaries
- Strings operations
- Bit and Boolean operations
- Flow Control
- Input/Output

## Installation

1. Ensure you have Python installed on your system.
2. Install the required dependencies by running:
   ```bash
   pip3 install pytest
3. Download or clone this repository to your local machine.

## How to run and use postscript intrepreter

1. Run the postscript intrepreter using the following command:
   ```bash
   python3 psip.py
2. Run the postscript intrepreter pytest using the following command:
   ```bash
   pytest test_psip.py
3. Swap between Lexical and Dynamic Scoping by changing isDynamic to True or False
4. Enter one input at a time
5. Ensure you have the correct number of arguments in stack before entering an operation
6. Hit = or == to print to the screen the result or what is on the top of the stack

## Program Mechanics
- User inputs get pushed into the stack
- Operations consume what is on the stack based on the arguments they take by popping them off
- Results get pushed into the stack after the operation

## Dependencies
- Python 3.x
- pytest

