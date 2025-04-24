import logging
import math
import re
logging.basicConfig(level = logging.DEBUG) #INFO, DEBUG

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

#For stack operations
class StackEmpty(Exception):
    """Exception with stack being empty"""
    def __init__(self, message):
        super().__init__(message)

#For copy operation in stack manipulation, if number is greater than length of stack
class GreaterThanStack(Exception):
    """Number is greater than length of stack"""
    def __init__(self, message):
        super().__init__(message)

class NotAnIntegerArg(Exception):
    """operations that require int's as arguments"""
    def __init__(self, message):
        super().__init__(message)

class DictNode:
    def __init__(self, limit, definedDict):
        self.mDict = {}
        self.count = 0
        self.limit = limit
        self.definedDict = definedDict
        logging.debug(f"Dict created with {limit} limit")

    def insert(self, key, value):
        self.mDict[key] = value
        self.count += 1
    
    def remove(self, key):
        self.mDict.pop(key)
        self.count -= 1

    def count(self):
        return self.count
    
    def __repr__(self):
        return "--dict--"

#Node Class to store a dictionary
class DictList:
    def __init__(self):
        self.gList = []
    
    def insertDict(self, newDict):
        self.gList.append(newDict)
    
    def popDict(self):
        if (self.count != 0):
            self.gList.pop()

    def accessPrev(self, currIndex):
        if (currIndex >= 0):
            return self.gList[currIndex]
    
    # def find(self, currDict):
    #     for d in self.gList:
    #         if d == currDict:
    #             return d

    #     return False     
        
dict_tracker = DictList()
dict_tracker.insertDict((dict_stack[-1]))

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
            # if(input[1: -1].startswith("(") and input[1:-1].endswith(")")): #if inner code contains a string only, needed for conditional
            #     return input[1:-1]
            # else:
            rInner = re.findall(r'\([^\)]+\)|=|\S+', input[1:-1])
            print(f"this is rInner: {rInner}")
            print(f"This is input{input[1: -1].strip().split()}")
            return rInner#input[1: -1].strip().split()
    else:
        raise ParseFailed("Can't parse this into a code block")

def process_name_constant(input):
    logging.debug(f"Input to process number: {input}")
    if input.startswith("/"):
        return input
    else:
        raise ParseFailed("Can't parse into name constant")
    
def process_string_input(input):
    logging.debug(f"Input to process string: {input}")
    if input.startswith("("):
        return input
    else:
        raise ParseFailed("Can't parse into string")

def process_list_input(input):
    logging.debug(f"Input to process list: {input}")
    if input.startswith("["):
        return input
    else:
        raise ParseFailed("Can't parse into list")
    
# def process_dict_input(input):
#     logging.debug(f"Input to process dict: {input}")
#     if isinstance(input, dict):
#         return input
#     else:
#         raise ParseFailed("Can't parse into dict")

PARSERS = [
    process_boolean,
    process_number,
    process_code_block,
    process_name_constant,
    process_string_input,
    process_list_input,
    #process_dict_input

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

############################## Arithmetic Operations start #################################
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

#Floor operation will round down to the nearest whole number
def floor_operation():
    if(len(op_stack) >= 1):
        num = op_stack.pop()
        res = float(math.floor(num))
        op_stack.append(res)
    else:
        raise TypeMismatch("Not enough operands for operation abs")

dict_stack[-1]["floor"] = floor_operation

#Round operation will round down if decimal is less than .5, will round up if
#it is .5 or higher
def round_operation():
    if(len(op_stack) >= 1):
        num = op_stack.pop()
        res = float(round(num))
        op_stack.append(res)
    else:
        raise TypeMismatch("Not enough operands for operation abs")

dict_stack[-1]["round"] = round_operation

def sqrt_operation():
    if(len(op_stack) >= 1):
        if (op_stack[-1] >=0):
            num = op_stack.pop()
            res = math.sqrt(num)
            op_stack.append(res)
        else:
            raise Exception("Can't take sqrt of negative numbers!")
    else:
        raise TypeMismatch("Not enough operands for operation abs")

dict_stack[-1]["sqrt"] = sqrt_operation

############# End of Arithmetic Operations #################

#Operation to define variables
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

######################### Stack Operations Begin #######################################

def pop_and_print():
    if(len(op_stack) >= 1):
        op1 = op_stack.pop()
        if isinstance(op1, str): #take out parenthesis of strings
            if (op1.startswith("(") and op1.endswith(")")):
                op1 = op1[1:-1]
                print(op1)
            elif (op1.startswith("[") and op1.endswith("]")): #refers to list
                print("--nostringval--")
        elif isinstance(op1, list): #refers to codeblocks
            print("--nostringval--")
        else:
            print(op1)
    else:
        raise StackEmpty("Stack is empty! Nothing to print")

dict_stack[-1]["="] = pop_and_print

def pop_and_print2():
    if(len(op_stack) >= 1):
        op1 = op_stack.pop()

        if isinstance(op1, list):
            res = "{"
            for item in op1:
                res += f"{item} "
            res = res[0:-1] + "}"
            print(res)
        else:
            print(op1)
    else:
        raise StackEmpty("Stack is empty! Nothing to print")
dict_stack[-1]["=="] = pop_and_print2

def exch_operation():
    if (len(op_stack) >= 2):
        num1 = op_stack.pop() #Top of stack
        num2 = op_stack.pop() #Next in line
        op_stack.append(num1)
        op_stack.append(num2)
    else:
        raise StackEmpty("Stack is empty, nothing to exchange")

dict_stack[-1]["exch"] = exch_operation

def pop_operation():
    if (len(op_stack) >= 1):
        op_stack.pop()
    else:
        raise StackEmpty("Stack is empty, nothing to pop")

dict_stack[-1]["pop"] = pop_operation

def dup_operation():
    if (len(op_stack) > 0):
        num = op_stack.pop()
        op_stack.append(num)
        op_stack.append(num)
    else:
        raise StackEmpty("Stack is empty, nothing to dup")

dict_stack[-1]["dup"] = dup_operation

def clear_operation():
    op_stack.clear()

dict_stack[-1]["clear"] = clear_operation

def count_operation():
    count = len(op_stack)
    op_stack.append(count)

dict_stack[-1]["count"] = count_operation

def copy_operation():
    copyList = []

    if(len(op_stack) > 0):
        if(op_stack[-1] < len(op_stack)): #if amount to copy is less than stack length
            amount = op_stack.pop()

            while(amount > 0):
                copyList.append(op_stack.pop())
                amount -= 1
            
            i = -(len(copyList)) - 1
            j = -1
            while (j > i):
                op_stack.append(copyList[j])
                j -= 1

            while(len(copyList) > 0):
                op_stack.append(copyList.pop())

        else:
            raise GreaterThanStack("Number greater than stack length!")
    else:
        raise StackEmpty("Stack empty, nothing to copy!")

dict_stack[-1]["copy"] = copy_operation

######################### Stack Operations End ############################################

######################### Dictionary Operations Begin #####################################

#This is what will go through and check the dictionary to see if it is callable
#If it is not callable, then it will check the instance, and process input,
#otherwise it is a value and will append to the stack.
def lookup_in_dictionary(input):#modify this
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
    
def dict_operation():
    if (len(op_stack) > 0):
        num = op_stack.pop()
        print(num)
        if (num >= 0):
            nDict = DictNode(num, dict_stack[-1])
            dict_tracker.insertDict(nDict)
            op_stack.append(nDict)
        else:
            op_stack.append(num) #put number back in stack
    else:
        raise StackEmpty("Stack is empty, unable to create dictionary!")

dict_stack[-1]["dict"] = dict_operation

def dict_length_op():
    if (isinstance(dict_stack[-1], dict)):
        op_stack.append(len(dict_stack[-1]))
    elif (isinstance(dict_stack[-1], DictNode)):
        op_stack.append(dict_stack[-1].count())
    else: #empty will add 0 to stack
        op_stack.append(0)
    
dict_stack[-1]["dict length"] = dict_length_op

def dict_maxlength_op():
    if (isinstance(dict_stack[-1], dict)):
        op_stack.append(200)
    elif (isinstance(dict_stack[-1], DictNode)):
       op_stack.append(dict_stack[-1].limit)
    else:
        raise Exception("Error finding dictionary!")
    
dict_stack[-1]["dict maxlength"] = dict_maxlength_op
    
#def begin_operation():

    #......

    
#dict_stack[-1]["begin"] = begin_operation
    
######################### Dictionary Operations End #####################################
    
#########################   String Operations Begin #####################################

#Gets the length of the string
def strLength():
    if (len(op_stack) > 0):
        if op_stack[-1].startswith("(") and op_stack[-1][1] != ")": #if starts with ( and index 1 is not )
            op_stack.append(len(op_stack.pop()) - 2)
        else:
            print(op_stack[-1][1]) #means they entered () aka an empty string
            op_stack.append(0)
    else:
        raise StackEmpty("Stack is empty, unable to get length of string")
dict_stack[-1]["length"] = strLength

#Gets substring of a string
def strGetInterval():
    if (len(op_stack) >= 3):
        result = ""
        traverse = op_stack.pop() #how much to copy over
        start = op_stack.pop() #start index
        if op_stack[-1].startswith("("): #if starts with (
            word = op_stack.pop() #copying word
            length = len(word)
            word = word[1:length - 1]

            if (traverse.is_integer() and start.is_integer()):
                if ((start+traverse) - 1 < length):
                        while (traverse > 0):
                            result += word[start]
                            start += 1
                            traverse -= 1
                        op_stack.append(result)
                else:
                    raise Exception("Interval greater than string length")
            else:
                raise NotAnIntegerArg("Not all arguments are integers")
        
    else:
        raise TypeMismatch("Not enough arguments in stack")
    
dict_stack[-1]["getinterval"] = strGetInterval

#Gets the character of the string based on the index, returns ascii value
def strGet():
    if (len(op_stack) >= 2):
        index = op_stack.pop()

        if op_stack[-1].startswith("(") and op_stack[-1][1] != ")": #if starts with (
            word = op_stack.pop() #copying word
            length = len(word)
            word = word[1:length - 1]

            if (index < length - 1):
                res = word[index]
                op_stack.append(ord(res))
            else:
                raise Exception("Index greater than length of string")
        else: # got the '()' input, which case we put back index
            op_stack.append(index)

    else:
        raise TypeMismatch("Not enough arguments in stack")
dict_stack[-1]["get"] = strGet

#Replaces substrings based on the index given. string2 must not be longer than string 1
def strPutInterval():
    if (len(op_stack) >= 3):
        string2 = op_stack.pop()
        startIndex = op_stack.pop()
        string1 = op_stack.pop()

        if(len(string2) <= len(string1) and startIndex.is_integer()): #If string2 is longer, will not process, checking if proper argument
            string1 = string1[1: len(string1) - 1] #Taking out parenthesis
            string2 = string2[1: len(string2) - 1] #Taking out parenthesis
            res = string1[0: startIndex]
            j = startIndex
            
            
            print(f"Before loop1: {res}")
            for i in string2:
                res += i
                j += 1
            
            print(f"After loop1: {res}, {j}")
            if (j < len(string1)): #If string2 is smaller, want to copy over rest of string 1
                while (j < len(string1)):
                    res += string1[j]
                    j +=1 

            op_stack.append(res)

        else:
            raise TypeMismatch("Is not a digit or string2 longer than string1")
            
    else:
        raise TypeMismatch("Not enough arguments in stack")
    
dict_stack[-1]["putinterval"] = strPutInterval

#Operation pops and prints strings in postscript only
def print_operation():
    if (len(op_stack) >= 1):
        string = op_stack.pop()

        if(isinstance(string, str)):
            if(string.startswith("(") and string.endswith(")")): #only printing if starts with parenthesis
                print(string[1:-1])
            else:
                op_stack.append(string) #put back in stack not a string value in postscript
    else:
        raise TypeMismatch("Not enough arguments in stack")
    
dict_stack[-1]["print"] = print_operation
######################### String Operations End #########################################

#########################   Bit & Bool Operations Begin #################################

#checks to see if inputs are equal
def eq_operation():
    if (len(op_stack) >= 2):
        var2 = op_stack.pop()
        var1 = op_stack.pop()

        if (var1 == var2):
            op_stack.append(True)
        else:
            op_stack.append(False)
    
    else:
        raise TypeMismatch("Not enough arguments in stack")
    
dict_stack[-1]["eq"] = eq_operation

#checks if var1 is not equal to var2
def ne_operation():
    if (len(op_stack) >= 2):
        var2 = op_stack.pop()
        var1 = op_stack.pop()

        if (var1 != var2):
            op_stack.append(True)
        else:
            op_stack.append(False)
    
    else:
        raise TypeMismatch("Not enough arguments in stack")
    
dict_stack[-1]["ne"] = ne_operation

#checks to see if var1 is greater or equal to var2
def ge_operation():
    if (len(op_stack) >= 2):
        var2 = op_stack.pop()
        var1 = op_stack.pop()

        if (var1 >= var2):
            op_stack.append(True)
        else:
            op_stack.append(False)
    
    else:
        raise TypeMismatch("Not enough arguments in stack")
    
dict_stack[-1]["ge"] = ge_operation

#checks to see if var1 is greater than var2
def gt_operation():
    if (len(op_stack) >= 2):
        var2 = op_stack.pop()
        var1 = op_stack.pop()

        if (var1 > var2):
            op_stack.append(True)
        else:
            op_stack.append(False)
    
    else:
        raise TypeMismatch("Not enough arguments in stack")
    
dict_stack[-1]["gt"] = gt_operation

#checks to see if var1 is less than or equal to var2
def le_operation():
    if (len(op_stack) >= 2):
        var2 = op_stack.pop()
        var1 = op_stack.pop()

        if (var1 <= var2):
            op_stack.append(True)
        else:
            op_stack.append(False)
    
    else:
        raise TypeMismatch("Not enough arguments in stack")
    
dict_stack[-1]["le"] = le_operation

#checks to see if var1 is less than var2
def lt_operation():
    if (len(op_stack) >= 2):
        var2 = op_stack.pop()
        var1 = op_stack.pop()

        if (var1 < var2):
            op_stack.append(True)
        else:
            op_stack.append(False)
    
    else:
        raise TypeMismatch("Not enough arguments in stack")
    
dict_stack[-1]["lt"] = lt_operation

#Performs logical and if its a bool and bitwise and if an integer
def and_operation():
    if (len(op_stack) >= 2):
        var2 = op_stack.pop()
        var1 = op_stack.pop()
        
        if(isinstance(var1, int) and isinstance(var2, int)):
            res = var1 & var2
            op_stack.append(res)
        elif (isinstance(var1, bool) and isinstance(var2, bool)):
            res = var1 and var2
            op_stack.append(res)
        else: #different types than what and can do, put back in stack and raise exception
            op_stack.append(var1)
            op_stack.append(var2)
            raise TypeMismatch("Not matching inputs or not of type int or bool")
            
    else:
        raise TypeMismatch("Not enough arguments in stack")
    
dict_stack[-1]["and"] = and_operation

#Performing bitwise not on integer inputs, and logical not on bools
def not_operation():
    if (len(op_stack) >= 1):
        var = op_stack.pop()

        if(isinstance(var, bool)):
            op_stack.append(not var)
        elif (isinstance(var, int)):
            op_stack.append(~var)
        else: #different types than what and can do, put back in stack and raise exception
            op_stack.append(var)
            raise TypeMismatch("Not valid input type")
    else:
        raise TypeMismatch("Not enough arguments in stack")
    
dict_stack[-1]["not"] = not_operation

#Performing bitwise and logical 'or' depending if input is integer or boolean
def or_operation():
    if (len(op_stack) >= 2):
        var2 = op_stack.pop()
        var1 = op_stack.pop()
        
        if(isinstance(var1, int) and isinstance(var2, int)):
            res = var1 | var2
            op_stack.append(res)
        elif (isinstance(var1, bool) and isinstance(var2, bool)):
            res = var1 or var2
            op_stack.append(res)
        else: #different types than what and can do, put back in stack and raise exception
            op_stack.append(var1)
            op_stack.append(var2)
            raise TypeMismatch("Not matching inputs or not of type int or bool")
            
    else:
        raise TypeMismatch("Not enough arguments in stack")
    
dict_stack[-1]["or"] = or_operation
#########################   Bit & Bool Operations End ###################################

#########################   Flow Control Operations Begin ###############################

#If conditional, if true will run code block, else nothing happens, stack gets emptied
def if_operation(): 
    if (len(op_stack) >= 2):
        output = op_stack.pop()
        bool_var = op_stack.pop()
        print(f"This is output {output}")
        print(type(output))
    

        if(bool_var):
            for i in output:
                process_input(i)
        else:
            raise TypeMismatch("Not valid arguments in stack")
        
    else:
        raise TypeMismatch("Not enough arguments in stack")

dict_stack[-1]["if"] = if_operation

#if true, will run one code block, else if will run the other code block
def ifelse_operation():
    if (len(op_stack) >= 3):
        outputTrue = op_stack.pop()
        outputFalse = op_stack.pop()
        bool_var = op_stack.pop()

        if(bool_var):
            for i in outputTrue:
                process_input(i)
        elif (bool_var == False):
            for j in outputFalse:
                process_input(j)
        else:
            raise TypeMismatch("Not valid arguments in stack")
        # if (isinstance(outputTrue, str) and isinstance(outputFalse, str) and isinstance(bool_var, bool)):
        #     if(bool_var):
        #         outputTrue = outputTrue[1:len(outputTrue) - 1]
        #         op_stack.append(outputTrue.strip())
        #     else:
        #         outputFalse = outputFalse[1:len(outputFalse) - 1]
        #         op_stack.append(outputFalse.strip())
        # else:
        #     raise TypeMismatch("Not valid arguments in stack")
        
    else:
        raise TypeMismatch("Not enough arguments in stack")

dict_stack[-1]["ifelse"] = ifelse_operation

# j is the intial value, k is the increment, l is the limit, proc is code block, for loop
def for_operation():
    if (len(op_stack) >= 4): #need j,k,l,procedure
        codeBlock = op_stack.pop()
        limit = op_stack.pop()
        increment = op_stack.pop()
        i = op_stack.pop()

        if (increment > 0): # postive increment
            for num in range(limit):
                process_input(i)
                for j in codeBlock:
                    process_input(j)
                i += increment
        else: #negative increment
            for num in range(i):
                process_input(i)
                for j in codeBlock:
                    process_input(j)
                i += increment
    else:
        raise TypeMismatch("Not enough arguments in stack")

dict_stack[-1]["for"] = for_operation

def repeat_operation():
    if (len(op_stack) >= 2): 
        codeBlock = op_stack.pop()
        iterations = op_stack.pop()

        if (iterations.is_integer() and iterations >= 0):
            for i in range(iterations):
                for items in codeBlock:
                    process_input(items)
    else:
        raise TypeMismatch("Not enough arguments in stack")

dict_stack[-1]["repeat"] = repeat_operation

#########################   Flow Control Operations End #################################

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

