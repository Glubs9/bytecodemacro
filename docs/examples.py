from bytecodemacro import * #probalby should individually import for readability but can't be bothered rn

#this example demonstrates a basic macro that doesn't perform any manipulation on the function but it does demonstrate how the tuple is structured
def macro_trace(tups):
    for n in tups: print(n)
    return tups

print("\nbefore macro trace")
@macro(macro_trace)
def test(a):
    print("a passed as " + str(a))
    return a
print(test(3))
print("after macro trace\n")


#this example adds an argument to a function
def add_arg(tups):
    ret = tups[:1]
    ret.append(("ADD_ARG", "a")) #adds extra argument a
    for n in tups[1:]: #could do with a list comprehension or map but this is easier to understand
        inst, arg = n
        if inst == "LOAD_NAME" and arg == "a":
            #replacing load_name with load_fast cause arguments have to be load_fast but the interpreter parses all mentions of a as load_name
            ret.append(("LOAD_FAST", "a")) 
        else:
            ret.append(n)
    return ret

@macro(add_arg)
def test(b):
    print("b passed as " + str(b))
    print("a passed as " + str(a))
print("\nbefore add_arg")
test(3, 4)
print("after add_arg\n")


def goto(tups):
    ret = []
    for n in tups:
        inst, arg = n
        if inst == "LOAD_CONST" and len(arg) > 6 and arg[1:5] == "goto":
            ret.append(("JUMP_ABSOLUTE", arg[6:-1]))
        elif inst == "LOAD_CONST" and len(arg) > 2 and arg[-2] == ":":
            ret.append(("LABEL", arg[1:-2]))
        else:
            ret.append(n)
    return ret

@macro(goto)
def f():
    n = 0
    while n < 10:
        if n > 5:
            _ = "goto exit"
        print(n)
        n+=1
    _ = "exit:"
print("\nbefore goto example")
f()
print("after goto\n")


def constant(tups_in):
    ret = []
    constants = {}
    for n in tups_in:
        inst, arg = n
        if inst == "LOAD_CONST" and len(arg) > 6 and arg[1:6] == "const":
            var_name, val = arg[7:-1].split(" ")
            if var_name not in constants:
                constants[var_name] = val
            else:
                raise Exception("tried to redefine a constant")
        elif arg in constants:
            ret.append(("LOAD_CONST", constants[var_name]))
        else:
            ret.append(n)
    return ret

@macro(constant)
def test():
    _ = "const x 15" #note: x is only available in this scope
    print(x)
    x = 100
    print(x) #15 because x is constant set to 15
    #_ = "const x 100" #error because you cannot redefine a constant

print("\nbefore constant")
test()
print("after constant\n")


def split(string_in):
    return string_in.split(";")

def cloop(tups):
    ret = []
    for_iterator = []
    checker = []
    for n in tups:
        if len(n) > 2: #fix later
            ret.append(n)
            continue
        inst, arg = n
        if arg == "_": continue #just cause my code is bad lmao
        elif inst == "LOAD_CONST" and len(arg) > 3 and arg[1:4] == "for":
            definition, check, iterator = tuple(split(arg[5:-1]))
            ret += byte_compile(definition)
            ret.append(("LABEL", "for"))
            for_iterator = byte_compile(iterator)
            checker = byte_compile(check)[:-1] #pops the result of comparison
        elif inst == "LOAD_CONST" and arg == '"end"':
            ret += for_iterator
            ret += checker
            ret.append(("POP_JUMP_IF_TRUE", "for"))
        else:
            ret.append(n)
    return ret

@macro(cloop)
def test(a):
    _ = "for c = 0;c < a;c+=1"
    print(c)
    _ = "end"
print("\nbefore cloop")
test(10)
print("after cloop\n")


"""
#doesn't work right now, probably a bug or something

def walrus(tups):
    ret = []
    for n in tups:
        inst, arg = n
        if inst == "LOAD_CONST":
            #poorly named variables
            tmp = arg.split(" ")
            if len(tmp) >= 2 and tmp[1] == ":=":
                tmp2 = byte_compile(" ".join(tmp[2:-1]) + " " + tmp[-1][:-1]) #last one removes the extra " (might create extra space in string?)
                if len(tmp2[-1]) > 1 and tmp2[-1][1] == "__doc__": tmp2 = tmp2[:-1] #idk whats happening here
                ret += tmp2
                var_name = unused_var(tups, ret)
                ret.append(("STORE_FAST", var_name)) #change to new_var later
                ret.append(("LOAD_FAST", var_name)) #change to new_var later
                ret.append(("STORE_NAME", tmp[0][1:])) #remove extra "
                ret.append(("LOAD_FAST", var_name)) #adds extra walrus to stack
            else:
                ret.append(n)
        else:
            ret.append(n)
    print(ret)
    return ret

@macro(walrus)
def test(): #should print hello world twice
    print("x := 'hello world'")
    if x == "hello world":
        print("walrus successful!")
    else:
        print("oops")
test()
"""

def add(tups):
    ret = []
    for n in tups:
        inst, arg = n
        if inst == "LOAD_CONST" and len(arg) > 4 and arg[1:4] == "add":
            ret += byte_compile(arg[5:-1])
        else:
            ret.append(n)
    return ret

@macro(add)
def test():
    _ = "add print('hello world')"
print("\nbefore test")
test()
print("after test\n")
