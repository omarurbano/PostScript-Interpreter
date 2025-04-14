import psip
import pytest

def test_add_operation():
    psip.op_stack.clear()
    psip.process_input("1")
    psip.process_input("2")
    psip.process_input("add")
    assert psip.op_stack[-1] == 3

def test_lookup_operation():
    psip.op_stack.clear()
    psip.process_input("/x")
    psip.process_input("2")
    psip.process_input("def")
    psip.process_input("x")
    assert psip.op_stack[-1] == 2

#dealing with negative numbers, making sure everything is in the correct 
#order
def test_sub_operation():
    psip.op_stack.clear()
    psip.process_input("10")
    psip.process_input("20")
    psip.process_input("sub")
    assert psip.op_stack[-1] == -10

    psip.op_stack.clear()
    psip.process_input("20")
    psip.process_input("10")
    psip.process_input("sub")
    assert psip.op_stack[-1] == 10

    psip.op_stack.clear()
    psip.process_input("20000000000000.0")
    psip.process_input("10000000000000.0")
    psip.process_input("sub")
    assert psip.op_stack[-1] == 10000000000000.0

#Testing multiplication operation
def test_mul_operation():
    psip.op_stack.clear()
    psip.process_input("1")
    psip.process_input("0")
    psip.process_input("mul")
    assert psip.op_stack[-1] == 0

    psip.op_stack.clear()
    psip.process_input("20")
    psip.process_input("10.0")
    psip.process_input("mul")
    assert psip.op_stack[-1] == 200.0

    psip.op_stack.clear()
    psip.process_input("20000000000000")
    psip.process_input("2")
    psip.process_input("mul")
    assert psip.op_stack[-1] == 40000000000000
    
#Testing Division operation
def test_div_operation():
    psip.op_stack.clear()
    psip.process_input("0")
    psip.process_input("1")
    psip.process_input("div")
    assert psip.op_stack[-1] == 0.0

    psip.op_stack.clear()
    psip.process_input("10.0")
    psip.process_input("20")
    psip.process_input("div")
    assert psip.op_stack[-1] == 0.5

    #Division by zero will make sure the numbers are back on the stack
    psip.op_stack.clear()
    psip.process_input("2")
    psip.process_input("0")
    psip.process_input("div")
    assert len(psip.op_stack) == 2 #checking length of stack
    
#Testing mod operation
def test_mod_operation():
    psip.op_stack.clear()
    psip.process_input("10")
    psip.process_input("2")
    psip.process_input("mod")
    assert psip.op_stack[-1] == 0

    psip.op_stack.clear()
    psip.process_input("11")
    psip.process_input("2")
    psip.process_input("mod")
    assert psip.op_stack[-1] == 1

    psip.op_stack.clear()
    psip.process_input("10")
    psip.process_input("-3")
    psip.process_input("mod")
    assert psip.op_stack[-1] == -2

    #mod by zero will make sure the numbers are back on the stack
    psip.op_stack.clear()
    psip.process_input("2")
    psip.process_input("0")
    psip.process_input("mod")
    assert len(psip.op_stack) == 2 #checking length of stack