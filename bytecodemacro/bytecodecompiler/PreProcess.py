#this file takes code context in with a string bytecode and converts it to a list of tuples that are
    #properly formatted with byte arguments as opposed to the previous string arguments

from functools import partial
from bytecodemacro.bytecodecompiler.CodeContext import CodeContext
from bytecodemacro.common.functional import bind, compose

#this function takes in a code object and a list of all the code objects and returns the same code
#object with a processed bytecode and attributes that match (like the consts array holds constants).
    #the reason it is a massive closure is because due to the nature of the bytecode, writing this
    #with state makes more sense and as this function can be called multiple times it's better to
    #keep the state in the function so that it is remade and not kept the same between objects
    #although this function is quite ugly as far as coding goes, especially with all that state.
    #hopefully there is a better way to do this but I can't think of one without seriously downsides
def PreProcess(code_context_in, all_objects):

    #the naming schema is a bit weird with these lists but it is to keep it consistent with the
    #documentations (in the dis library) names
    constants = [] #list of literals used in the program (i would use a set for faster seraching but the instructions rely on the index of the literal so i have to)
    names = [] #list of names used in the program (same logic about sets as above)
    varnames = code_context_in.varnames #(the arguments already exist as varnames)
    global_list = [] #although in documentation this is globals but I can't name it that due to globals being reserved
    cellvars = [] #not sure what this is (this is the freevars storage but i'm not sure how to do this)

    compare_list = ('<', '<=', '==', '!=', '>', '>=') 
    label_positions = {}

    #this function takes a line and returns a boolean if it should be removed from the bytecode
    def should_remove(line): #called in the filter function
        if len(line) == 0: return False #this is already done in parse but i've kept it here just in case i delete it there
        elif line[0][0] == "#": return False #manual comments in the code, note: this could be deleted
        else: return True

    #this function finds all of the labels, changes them to nop and adds there positions to label_positions
    def find_labels(lines): #not a massive fan of this function but it works
        ret = []
        for i, v in enumerate(lines):
            if len(v) == 2 and v[0] == "LABEL":
                label_positions[v[1]] = i*2 #*2 because it is the position in the byte string and
                                              #it is 2 bytes per instruction
                v = ["NOP"]
            ret+=[v]
        return ret

    #removes any empty arguments in a tuple
    def clean_args(val):
        if len(val) == 1: return val
        if val[1] == '':  return [val[0]]
        else:             return val[:2]

    #for instrucitons that don't have arguments (like pop_top or return_value)
        #note: this is not likely to occur in the context of a macro
    def add_arg(val):
        if len(val) == 1: 
            return val + [0]
        return val

    #when an instruction is called that its argument is an index to a list attribute in the original
    #bytecode, this function is used to add that argument to the attribute in the new bytecode when
    #we are generating it, this also prevents the same argument from getting added to the bytecode
    #attributes more than once
    #e.g: load_const "hello world" will add hello world to the constants array and return load_const 1
    def memoize_loading(lis, arg): #note: memoize loading is called sometimes with things that should not be added to (what does this mean?)
        try: 
            arg = int(arg)
        except ValueError:
            try:
                arg = float(arg)
            except ValueError: pass
        finally:
            if arg in lis: arg = lis.index(arg) #double check later, also very slow
            else: lis.append(arg); arg = len(lis)-1 #maybe remove semi colon but I like how this looks
            return (lis, arg)

    #commands to lists is used in handle_literals
        #note: i am not sure how load_closurer works and it has something weird about freevars in it
    commands_to_lists = {"LOAD_CONST": constants, "LOAD_NAME": names, "LOAD_GLOBAL":
            global_list, "LOAD_FAST": varnames, "STORE_FAST": varnames, "DELETE_FAST":
            varnames, "LOAD_ATTR": names,
            "LOAD_CLOSURE": cellvars, "LOAD_DEREF": cellvars, "LOAD_CLASSDEREF": cellvars,
            "DELETE_DEREF": cellvars, "LOAD_METHOD": names, "STORE_NAME": names,
            "STORE_ATTR": names, "STORE_GLOBAL": global_list, "STORE_DEREF": cellvars,
            "DELETE_NAME": names, "DELETE_ATTR": names, "DELETE_GLOBAL": global_list,
            "IMPORT_NAME": names, "IMPORT_FROM": names, "COMPARE_OP": compare_list}
    #this function will take an instructino and if it contains an instruction that would normally
    #index into an attribute of an array in the original bytecode, it calls memoize_loading to handle it
    def handle_literals(val):
        inst, arg = val
        if inst in commands_to_lists:
            lis = commands_to_lists[inst]
            lis, arg = memoize_loading(lis, arg)
        return (inst, arg)

    #this function takes a line and if it is a jump absolute literal (with an absolute position in the
    #byetcode), and converts the second argument into the correct position in the code rather than the label
        #references a dictionary not a list so it has to be done like this (what does this mean?)
    def handle_jump_absolute_literals(line):
        inst, arg = line
        if inst in {"POP_JUMP_IF_TRUE", "POP_JUMP_IF_FALSE", "JUMP_IF_NOT_EXC_MATCH", "JUMP_IF_TRUE_OR_POP", "JUMP_IF_FALSE_OR_POP", "JUMP_ABSOLUTE"}:
            arg = label_positions[arg]
        return (inst, arg)

    #obj_dict is useful in handle_load_object
    obj_dict = {o[0].name: o for o in all_objects}
    #this function handle the custom instruciton load_object
    #it takes a line in and if that line is load_object it will load the constant object in
        #this function is not too useful in a macro, so it might have to be deleted in a later version
    def handle_load_object(line): 
        nonlocal constants
        inst, arg = line
        if inst == "LOAD_OBJECT":
            inst = "LOAD_CONST" #how this works is it first loads the object as a constant, but this
                                #object is in a one long array, as to emulate pointer behaviour in python to allow for recursive objects
                                #it also makes compilation of the objects a lot easier
            constants, arg = memoize_loading(constants, obj_dict[arg])
            inst2 = "LOAD_CONST" #it then loads 0 onto the stack
            constants, arg2 = memoize_loading(constants, 0) #i should be calling handle_literals instead of this, but tbh at this point i just don't care
            return [(inst, arg), (inst2, arg2), ("BINARY_SUBSCR",0)] #it then subscripts into the one length array to extract the python code object onto the stack
        return [(inst, arg)]

    #this function handles jumps statements that their arguments are relative jumps
    def handle_jump_relative_literals(lines):
        ret = []
        for i, v in enumerate(lines):
            inst, arg = v
            if inst in {"SETUP_WITH", "JUMP_FORWARD", "FOR_ITER", "SETUP_FNIALLY"}:
                arg = label_positions[arg] - i*2 #i*2 as there are two bytes per instruction
            ret += [(inst, arg)]
        return ret

    #used in debugging 
    def trace(v):
        print(v)
        return v

    #sometimes instructions need to be added after the labels positions have been defined in the
    #label position object so this function updates those labels to be in the correct spot
    def increment_labels_below(index, n):
        nonlocal label_positions
        label_positions = {key: val if val < index else val + n*2 for key, val in label_positions.items()} #n * 2 as instructions are 2 bytes long

    #this function checks to see if any argument in the tuple is above 255 and if it is it adds
    #extended arg instructions to ensure that the arguments are always byte sized
        #terrible name for a function
    def extended_args_instructions(n): #i like this functions implementation :)
        if n < 256: return [("EXTENDED_ARG", n)]
        if n > 255: 
            tmp = ("EXTENDED_ARG", n % 256)
            return [tmp] + extended_args_instructions(n >> 8)

    #this function takes in the byte tuples and if any argument is above byte sized, it adds
    #extended args instructions to the bytecode.
        #this function does none of the maths but it calls the extended_args_instruction function
        #which handles all of the hard work
    def handle_extended_args(lines):
        ret = []
        for i, v in enumerate(lines):
            inst, arg = v 
            if arg > 255: 
                e = extended_args_instructions(arg >> 8)
                increment_labels_below(i, len(e))
                arg = arg % 256
                ret += e
            ret.append((inst, arg))
        return ret

    #this creates a function pre_process that pre_processes a bytecode tuple
        #maybe not the cleanest to do it like this but it's more fun like this (i made this before I
            #knew other people were going to see this), it is probably worth changing as it's not the most readable
        #the order of the functions here is not completely arbitrary and any changes to this order
            #must be properly thought out
    pre_process = compose(
        partial(filter, should_remove),
        find_labels, #this can't be in the map cause it needs to have index information
        partial(map, compose(
            clean_args,
            add_arg, 
            lambda n: (n[0].upper(), n[1]), #makes the instructions uppercase (has to be a lambda cause .upper is a method (ruins my pointfree >:(
            handle_literals,
            handle_jump_absolute_literals
        )), #composes all the preproccessing that only needs a single line and not the context of other lines
        partial(bind, handle_load_object),
        handle_jump_relative_literals,
        partial(map, lambda n: (n[0], int(n[1]))),
        handle_extended_args,
        list #list might not be necersarry, but it's better safe than sorry in future updates
    )

    #this section of the code modifies all of the attributes of the code_context to their properly pre_processed version
    code_context_in.bytes = pre_process(code_context_in.bytes)
    code_context_in.constants = constants
    code_context_in.names = names
    code_context_in.global_list = global_list
    code_context_in.cellvars = cellvars
    code_context_in.varnames = varnames
