#this is some of the globals that are added to the code object in compilation
#many of them need to get affected by some of the instructions so I have made them mutable
#globals
    #THIS IS UGLY CODE AND IF I COULD THINK OF A CLEANER WAY TO DO THIS I WOULD BE THIS IS THE
    #ONLY WAY I CAN REALLY THINK OF THAT IS CLEAR AND OBVIOUS
        #woops caps lock
        #i could do this with my own code object and messing wit hthat but that would maybe be better code?
        #NOTE: potentially change this to be using a struct to store data rather than globals

#this file is only as long as it is cause of my ranting comments

from functools import reduce, partial
from bytecodemacro.bytecodecompiler.CodeContext import CodeContext

#the public preprocessing to be called
    #i'm not sure if chucking everything into a function like this is good or bad practice but i'm
    #doing it to keep my algorithm nice and clean
#this function could also be conceptualized as compiling an intermediary language (which is closer
            #to the output of dis)
def PreProcess(code_context_in, all_objects):

    #the naming schema is a bit weird with these lists but it is to keep it consistent with the
    #documentations (in the dis library) names
    constants = [] #list of literals used in the program (i would use a set for faster seraching but the instructions rely on the index of the literal so i have to 
    names = [] #list of names used in the program (same logic about sets as above)
    varnames = code_context_in.varnames #( the arguments already exist as varnames)
    global_list = [] #not called globals cause its reserved (also not sure it's necersarry, i'm a bit confused about store_global
    cellvars = [] #not sure what this is

    #below this line is globals that aren't returned but just used in preprocessing
    compare_list = ('<', '<=', '==', '!=', '>', '>=') 
    label_positions = {}

    #used to compose the pre-processing functions together
    def compose_list(f_list):
        def ret(arg):
            #probably a better way to do this (like a fold probaly?)
            return reduce(lambda a,n: n(a), f_list, arg)
        return ret

    def bind(f, li):
        return list(reduce(lambda a1,a2: a1+a2, map(f, li))) #not fast but it's elegant

    def should_remove(line): #called in the filter function
        if len(line) == 0: return False #this is already done in parse but i've kept it here just in
                                        #case i delete it
        if line[0][0] == "#": return False
        return True

    def find_labels(lines):
        #not a massive fan of this function but it works
            #i could do something with 
        ret = []
        for i, v in enumerate(lines):
            if len(v) == 2 and v[0] == "LABEL":
                label_positions[v[1]] = i*2 #*2 because it is the position in the byte string and
                                              #it is 2 bytes per instruction
                v = ["NOP"]
            ret+=[v]
        return ret

    #removes any empty arguments
    def clean_args(val):
        if len(val) == 1: return val
        if val[1] == '':  return [val[0]]
        else:             return val[:2]

    #for instrucitons that don't have arguments (like pop_top or return_value)
    def add_arg(val):
        if len(val) == 1: 
            return val + [0]
        return val

    def memoize_loading(lis, arg): #note: memoize loading is called sometimes with things that should not be added to 
        try: 
            arg = int(arg)
        except ValueError:
            try:
                arg = float(arg)
            except ValueError: pass
        finally:
            if arg in lis: arg = lis.index(arg) #double check later
            else: lis.append(arg); arg = len(lis)-1 #maybe remove semi colon
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
    def handle_literals(val):
        inst, arg = val
        if inst in commands_to_lists: #might have to nonlocal the commands_to_lists
            lis = commands_to_lists[inst]
            lis, arg = memoize_loading(lis, arg)
        return (inst, arg)

    #references a dictionary not a list so it has to be done like this
    #i have to handle jump_relatives (e.g: jump_forward) in a different function
    def handle_jump_absolute_literals(line):
        inst, arg = line
        if inst in {"POP_JUMP_IF_TRUE", "POP_JUMP_IF_FALSE", "JUMP_IF_NOT_EXC_MATCH", "JUMP_IF_TRUE_OR_POP", "JUMP_IF_FALSE_OR_POP", "JUMP_ABSOLUTE"}:
            arg = label_positions[arg]
        return (inst, arg)

    obj_dict = {o[0].name: o for o in all_objects}
    def handle_load_object(line):
        nonlocal constants
        inst, arg = line
        if inst == "LOAD_OBJECT":
            inst = "LOAD_CONST"
            constants, arg = memoize_loading(constants, obj_dict[arg])
            inst2 = "LOAD_CONST"
            constants, arg2 = memoize_loading(constants, 0) #i should be calling handle_literals instead of this, but tbh at this point i just don't care
            #the reason we have objects stored in a list and then subscripted is too emulate pointer
            #behaviour for later on so we can have cyclic references and the like, if you want a
            #more detailed explanation, give us an email: jonte.fry@gmail.com
            return [(inst, arg), (inst2, arg2), ("BINARY_SUBSCR",0)]
        else:
            return [(inst, arg)]

    def handle_jump_relative_literals(lines):
        ret = []
        for i, v in enumerate(lines):
            inst, arg = v
            if inst in {"SETUP_WITH", "JUMP_FORWARD", "FOR_ITER", "SETUP_FNIALLY"}:
                arg = label_positions[arg] - i*2 #i*2 as there are two bytes per instruction
            ret += [(inst, arg)]
        return ret

    #used in debugging (delete it later)
    def trace(v): #can't put in lambda cause one line
        print(v)
        return v

    def increment_labels_below(index, n):
        #sometimes insturctions need to be added after labels defined so they need to be updates
        nonlocal label_positions
        label_positions = {key: val if val < index else val + n*2 for key, val in label_positions.items()} #n * 2 as instructions are 2 bytes long

    #terrible name for a function
        #it's too early too think of anything good though
    def extended_args_instructions(n):
        if n < 256: return [("EXTENDED_ARG", n)]
        if n > 255: 
            tmp = ("EXTENDED_ARG", n % 256)
            return [tmp] + extended_args_instructions(n >> 8)

    #sometimes the arguments to an instruction become bigger then 255 (a byte) (particularly in jump
    #commands) so i have to add a thing to auto generate the extended args
        #i'm not a massive fan of this function, too much maths and i'm relying on calling the
        #funciton to execute some of the logic rather than the function wholeheartedly
        #i need to change this later
    def handle_extended_args(lines):
        ret = []
        for i, v in enumerate(lines):
            inst, arg = v 
            if arg > 255: 
                e = extended_args_instructions(arg >> 8)
                increment_labels_below(i, len(e))
                arg = arg % 256
                ret += e
            ret += [(inst, arg)]
        return ret

    #maybe not the cleanest to do it like this but it's more fun like this
        #the order of the functions here is not completely arbitrary but i can't be botehred figuring out the best way to do it
    pre_process = compose_list([
        partial(filter, should_remove),
        find_labels, #this can't be in the map cause it needs to have index information
        partial(map, compose_list([
            clean_args,
            add_arg, 
            lambda n: (n[0].upper(), n[1]), #makes the instructions uppercase (has to be a lambda cause .upper is a method (ruins my pointfree >:(
            handle_literals,
            handle_jump_absolute_literals
        ])), #composes all the preproccessing that only needs a single line and not the context of other lines
        partial(bind, handle_load_object),
        handle_jump_relative_literals,
        partial(map, lambda n: (n[0], int(n[1]))),
        handle_extended_args,
        list #list might not be necersarry, but it's better safe than sorry in future updates
    ])

    #look what you have done to me oo
    code_context_in.bytes = pre_process(code_context_in.bytes)
    code_context_in.constants = constants
    code_context_in.names = names
    code_context_in.global_list = global_list
    code_context_in.cellvars = cellvars
    code_context_in.varnames = varnames
