import logging
import math
logging.basicConfig(level = logging.INFO) #INFO, DEBUG

op_stack = []

dict_stack = []
dict_stack.append({})

class ParseFailed(Exception):
    """Exception while parsing"""
    def __init__(self, message):
        super().__init__(message)

class TypeMismatch(Exception):
    """Exception with types of operators and operands"""
    def __init__(self, message):
        super().__init__(message)

def repl():
    while True:
        user_input = input("REPL> ")
        if user_input.lower() == "quit":
            break
        process_input(user_input)
        logging.debug(f"Operand Stack: {op_stack}")

def process_boolean(input):
    logging.debug(f"Input to process boolean: {input}")
    if input == "true":
        return True
    elif input == "false":
        return False
    else:
        raise ParseFailed("Can't parse it into boolean")
    
def process_number(input):
    logging.debug(f"Input to process boolean: {input}")
    try:
        float_value = float(input)
        if float_value.is_integer():
            return int(float_value)
        else:
            return float_value
    except ValueError:
        raise ParseFailed("Can't parse this into a number")

def process_code_block(input):
    logging.debug(f"Input to process number: {input}")
    if len(input) >= 2 and input.startswith("{") and input.endswith("}"):
        return input[1: -1].strip().split()
    else:
        raise ParseFailed("Can't parse this into a code block")

def process_name_constant(input):
    logging.debug(f"Input to process number: {input}")
    if input.startswith("/"):
        return input
    else:
        raise ParseFailed("Can't parse into name constant")

PARSERS = [
    process_boolean,
    process_number,
    process_code_block,
    process_name_constant

]

def process_constants(input):
    # try:
    #     res = process_boolean(input)
    #     op_stack.append(res)
    # except ParseFailed as e:
    #     logging.debug(e)
    for parser in PARSERS:
        try:
            result = parser(input)
            op_stack.append(result)
            return
        except ParseFailed as e:
            logging.debug(e)
            continue
    raise ParseFailed(f"None of the parsers worked for the input {input}")

######## Operations start ##################
def add_operation():
    if(len(op_stack) >= 2):
        op1 = op_stack.pop()
        op2 = op_stack.pop()
        res = op1 + op2 #order here doesn't matter because of addition
        op_stack.append(res)

    else:
        raise TypeMismatch("Not enough operands for operation add")
    
dict_stack[-1]["add"] = add_operation

def sub_operation():
    if(len(op_stack) >= 2):
        num1 = op_stack.pop()
        num2 = op_stack.pop()
        res = num2 - num1 #num2 must be first, as that was added first
        op_stack.append(res)

    else:
        raise TypeMismatch("Not enough operands for operation sub")
    
dict_stack[-1]["sub"] = sub_operation

def mul_operation():
    if(len(op_stack) >= 2):
        num1 = op_stack.pop()
        num2 = op_stack.pop()
        res = num2 * num1
        op_stack.append(res)
    else:
        raise TypeMismatch("Not enough operands for operation mul")

dict_stack[-1]["mul"] = mul_operation

def div_operation():
    if(len(op_stack) >= 2):
        num1 = op_stack.pop()
        num2 = op_stack.pop()

        if (num1 == 0): # put numbers back in stack
            op_stack.append(num2)
            op_stack.append(num1)
            raise ZeroDivisionError("division by zero error")
        else:
            res = num2 / num1
            op_stack.append(res)
    else:
        raise TypeMismatch("Not enough operands for operation div")

dict_stack[-1]["div"] = div_operation

def mod_operation():
    if(len(op_stack) >= 2):
        num1 = op_stack.pop()
        num2 = op_stack.pop()

        if (num1 == 0): #Puts back numbers back in the stack
            op_stack.append(num2)
            op_stack.append(num1)
            raise ZeroDivisionError("division by zero error")
        else:
            res = num2 % num1
            op_stack.append(res)
    else:
        raise TypeMismatch("Not enough operands for operation mod")

dict_stack[-1]["mod"] = mod_operation

#Integer division, basically rounds down to nearest whole number, same as div, but converts res to int
def idiv_operation():
    if(len(op_stack) >= 2):
        num1 = op_stack.pop()
        num2 = op_stack.pop()

        if (num1 == 0): # put numbers back in stack
            op_stack.append(num2)
            op_stack.append(num1)
            raise ZeroDivisionError("division by zero error")
        else:
            res = (int) (num2 / num1)
            op_stack.append(res)
    else:
        raise TypeMismatch("Not enough operands for operation div")

dict_stack[-1]["idiv"] = idiv_operation

#Absolute value operation which makes any negative number to postive.
#Stack must have at least one or more values
def abs_operation():
    if(len(op_stack) >= 1):
        num = op_stack.pop()
        res = abs(num)
        op_stack.append(res)
    else:
        raise TypeMismatch("Not enough operands for operation abs")

dict_stack[-1]["abs"] = abs_operation

#Opposite of abs operation, will make postive numbers to negative numbers
def neg_operation():
    if(len(op_stack) >= 1):
        num = op_stack.pop()
        res = -(num)
        op_stack.append(res)
    else:
        raise TypeMismatch("Not enough operands for operation abs")

dict_stack[-1]["neg"] = neg_operation

#Ceiling operation will round up to the nearest whole number
def ceiling_operation():
    if(len(op_stack) >= 1):
        num = op_stack.pop()
        res = float(math.ceil(num))
        op_stack.append(res)
    else:
        raise TypeMismatch("Not enough operands for operation abs")

dict_stack[-1]["ceiling"] = ceiling_operation

def def_operation():
    if(len(op_stack) >= 2):
        value = op_stack.pop()
        name = op_stack.pop()
        if isinstance(name, str) and name.startswith("/"):
            key = name[1:]
            dict_stack[-1][key] = value
        else:
            op_stack.append(name)
            op_stack.append(value)
        

    else:
        raise TypeMismatch("Not enoough operands for operation add")
    
dict_stack[-1]["def"] = def_operation


############# End of Operations #################

def pop_and_print():
    if(len(op_stack) >= 1):
        op1 = op_stack.pop()
        print(op1)
    else:
        raise TypeMismatch("Stack is empty! Nothing to print")

dict_stack[-1]["="] = pop_and_print

def lookup_in_dictionary(input):
    top_dict = dict_stack[-1]
    if input in top_dict:
        value = top_dict[input]
        if callable(value):
            value()
        elif isinstance(value, list):
            for item in value:
                process_input(item)

        else:
            op_stack.append(value)
    else:
        raise ParseFailed(f"Input {input} is not in dictionary")

def process_input(user_input):
    #print(user_input)
    try:
        process_constants(user_input)
    
    except ParseFailed as e:
        logging.debug(e)
        try:
            lookup_in_dictionary(user_input)
        except Exception as e:
            logging.error(e)





if __name__ == "__main__":
    repl()

