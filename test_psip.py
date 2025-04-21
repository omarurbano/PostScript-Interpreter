import psip
import pytest
import sys

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

#Testing Division operation
def test_idiv_operation():
    psip.op_stack.clear()
    psip.process_input("10")
    psip.process_input("3")
    psip.process_input("idiv")
    assert psip.op_stack[-1] == 3

    psip.op_stack.clear()
    psip.process_input("10.0")
    psip.process_input("20")
    psip.process_input("idiv")
    assert psip.op_stack[-1] == 0

    #Division by zero will make sure the numbers are back on the stack
    psip.op_stack.clear()
    psip.process_input("2")
    psip.process_input("0")
    psip.process_input("idiv")
    assert len(psip.op_stack) == 2 #checking length of stack

#Testing the absolute value operation
def test_abs_operation():
    psip.op_stack.clear()
    psip.process_input("-10")
    psip.process_input("abs")
    assert psip.op_stack[-1] == 10

    psip.op_stack.clear()
    psip.process_input("0")
    psip.process_input("abs")
    assert psip.op_stack[-1] == 0

    psip.op_stack.clear()
    psip.process_input(str(-sys.maxsize))
    psip.process_input("abs")
    assert psip.op_stack[-1] == sys.maxsize + 1 #negative is one less than postive max size

#Testing the absolute value operation
def test_neg_operation():
    psip.op_stack.clear()
    psip.process_input("10")
    psip.process_input("neg")
    assert psip.op_stack[-1] == -10

    psip.op_stack.clear()
    psip.process_input("0")
    psip.process_input("neg")
    assert psip.op_stack[-1] == 0

    psip.op_stack.clear()
    psip.process_input(str(sys.maxsize))
    psip.process_input("neg")
    assert psip.op_stack[-1] == -sys.maxsize-1 #negative is one less than postive max size

#Testing ceiling operation to see if value is rounded up to the nearest value.
def test_ceiling_operation():
    psip.op_stack.clear()
    psip.process_input("3.14")
    psip.process_input("ceiling")
    assert psip.op_stack[-1] == 4.0

    psip.op_stack.clear()
    psip.process_input("0.01")
    psip.process_input("ceiling")
    assert psip.op_stack[-1] == 1.0

    psip.op_stack.clear()
    psip.process_input(str(sys.maxsize - 0.1))
    psip.process_input("ceiling")
    assert psip.op_stack[-1] == float(sys.maxsize)

#Testing floor operation to see if values are rounded down to the nearest whole number
def test_floor_operation():
    psip.op_stack.clear()
    psip.process_input("3.14")
    psip.process_input("floor")
    assert psip.op_stack[-1] == 3.0

    psip.op_stack.clear()
    psip.process_input("0.01")
    psip.process_input("floor")
    assert psip.op_stack[-1] == 0.0

    psip.op_stack.clear()
    psip.process_input(str(sys.maxsize - 0.1))
    psip.process_input("ceiling")
    assert psip.op_stack[-1] == float(sys.maxsize - 1)

#Testing round operation based on decimal value anything below .5 and
#.5 and higher
def test_round_operation():
    psip.op_stack.clear()
    psip.process_input("3.49")
    psip.process_input("round")
    assert psip.op_stack[-1] == 3.0

    psip.op_stack.clear()
    psip.process_input("3.5")
    psip.process_input("round")
    assert psip.op_stack[-1] == 4.0

    psip.op_stack.clear()
    psip.process_input(str(sys.maxsize - 0.1)) #will round up
    psip.process_input("round")
    assert psip.op_stack[-1] == float(sys.maxsize)

    psip.op_stack.clear()
    psip.process_input(str(sys.maxsize - 0.6)) #will round down
    psip.process_input("round")
    assert psip.op_stack[-1] == float(sys.maxsize - 1)

#Testing to sqrt arthemtic is working properly
def testing_sqrt_operation():
    psip.op_stack.clear()
    psip.process_input("100")
    psip.process_input("sqrt")
    assert psip.op_stack[-1] == 10.0

    psip.op_stack.clear()
    psip.process_input("0")
    psip.process_input("sqrt")
    assert psip.op_stack[-1] == 0.0

    psip.op_stack.clear()
    psip.process_input("-10")
    psip.process_input("sqrt") #Shouldn't pop due to negative number
    assert len(psip.op_stack) == 1 

#Testing our exchance manipulation to see if things get swapped properly
def testing_exch_operation():
    psip.op_stack.clear()
    psip.process_input("1")
    psip.process_input("2")
    psip.process_input("exch")
    assert psip.op_stack[-1] == 1

    psip.op_stack.clear()
    psip.process_input("/x = 3")
    psip.process_input("/square {dup mul} def")
    psip.process_input("exch")
    assert psip.op_stack[-1] == "/x = 3"

    psip.op_stack.clear()
    psip.process_input("/x = 3")
    psip.process_input("exch")
    assert len(psip.op_stack) == 1

#Testing stack manipulation where we use the "pop" command to pop an item off the stack
def testing_pop_operation():
    psip.op_stack.clear()
    psip.process_input("1")
    psip.process_input("2")
    psip.process_input("3")
    psip.process_input("4")
    psip.process_input("pop")
    assert len(psip.op_stack) == 3
    psip.process_input("pop")
    assert len(psip.op_stack) == 2
    psip.process_input("pop")
    assert len(psip.op_stack) == 1
    psip.process_input("pop")
    assert len(psip.op_stack) == 0

#Testing stack manipulation where we duplicate the top of the stack
def testing_dup_operation():
    psip.op_stack.clear()
    psip.process_input("1")
    psip.process_input("dup")
    assert len(psip.op_stack) == 2

    psip.op_stack.clear()
    psip.process_input(str(sys.maxsize))
    psip.process_input("dup")
    assert len(psip.op_stack) == 2

    psip.op_stack.clear()
    psip.process_input("/x = 3 def")
    psip.process_input("dup")
    assert len(psip.op_stack) == 2

#Testing stack manipulation, where we see that we clear the entire stack empty
def testing_clear_operation():
    psip.op_stack.clear()
    for i in range(100000):
        psip.process_input(f"{i}")
    
    psip.process_input("clear")
    assert len(psip.op_stack) == 0

#Testing stack manipulation, where we count the number of items in stack and push the result
#to the top of the stack
def testing_counting_operation():
    psip.op_stack.clear()
    for i in range(100000):
        psip.process_input(f"{i}")
    
    psip.process_input("count")
    assert psip.op_stack[-1] == 100000

    psip.op_stack.clear()
    psip.process_input("count")
    assert psip.op_stack[-1] == 0

#Testing the copy stack manipulation to see if the correct number of items are copied over
def testing_copy_operation():
    psip.op_stack.clear()
    for i in range(5):
        psip.process_input(f"{i}")
    psip.process_input("10")
    psip.process_input("copy")
    assert len(psip.op_stack) == 6 #nothing got copied because number at top is greater than stack length

    psip.process_input("2")
    psip.process_input("copy")

    assert psip.op_stack[-1] == psip.op_stack[-1 -2]
    assert psip.op_stack[-2] == psip.op_stack[-2 - 2]

    psip.op_stack.clear()
    for i in range(1000):
        psip.process_input(f"{i}")
    psip.process_input("1000")
    psip.process_input("copy")
    assert len(psip.op_stack) == 2000

#Testing the to see if we get the correct length of a string
def testing_string_length():
    psip.op_stack.clear()
    psip.process_input("(Hello)")
    psip.process_input("length")
    assert psip.op_stack[-1] == 5

    psip.op_stack.clear()
    psip.process_input("length")
    assert len(psip.op_stack) == 0
    
    psip.op_stack.clear()
    psip.process_input("()")
    psip.process_input("length")
    assert psip.op_stack[-1] == 0

    psip.op_stack.clear()
    psip.process_input("(aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa)")
    psip.process_input("length")
    assert psip.op_stack[-1] == 40

#Testing to see if the start and amount to copy over produces the substrings we expect
def testing_getinterval():
    psip.op_stack.clear()
    psip.process_input("(Hello, World!)")
    psip.process_input("7")
    psip.process_input("5")
    psip.process_input("getinterval")
    assert psip.op_stack[-1] == "World"

    psip.op_stack.clear()
    psip.process_input("()")
    psip.process_input("0")
    psip.process_input("0")
    psip.process_input("getinterval")
    assert psip.op_stack[-1] == ""

    psip.op_stack.clear()
    psip.process_input("(I)")
    psip.process_input("0")
    psip.process_input("1")
    psip.process_input("getinterval")
    assert psip.op_stack[-1] == "I"

#Testing get string operation, gets the ascii value of index indicated from string
def testing_get():
    psip.op_stack.clear()
    psip.process_input("(Hello)")
    psip.process_input("0")
    psip.process_input("get")
    assert psip.op_stack[-1] == 72

    psip.op_stack.clear()
    psip.process_input("(Hello,)")
    psip.process_input("5")
    psip.process_input("get")
    assert psip.op_stack[-1] == 44

    psip.op_stack.clear()
    psip.process_input("( )")
    psip.process_input("0")
    psip.process_input("get")
    assert psip.op_stack[-1] == 32