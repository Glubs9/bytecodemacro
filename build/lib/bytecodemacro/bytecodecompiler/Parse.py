#split the line into a series of code objects
    #entry point labelled as main

from bytecodemacro.bytecodecompiler.CodeContext import CodeContext

def split(lines):
    """ 
    split splits the files into a series of lines for each object
    (how to handle the args in)
    (this takes already lexed information from the csv reader)
    """
    curr_obj = None #gets defined as a CodeContext
    all_objs = []
    for n in lines:
        if len(n) == 0 or n[0][0] == "#": continue #this is preprocessing which should be done in preprocess.py but
                                 #i'm doing it here because the parser requires thsi to functoin
        elif n[0].upper() == "DEFINE":
            #remove empty lines here to properly work
            args = [i for i in n[2:] if i != ""]
            curr_obj = CodeContext(name=n[1], arg_num=len(args), varnames=args)
        elif n[0].upper() == "END":
            all_objs += [curr_obj]
            curr_obj = None
        else:
            curr_obj.bytes += [n]
    return all_objs

#this should be in PreProcess but i put it in here because ?? (i mean it is small and elegant and i don't want to look at PreProccess rn tbh)
    #this takes an object, adds the arguments to the object, then returns it
    #*technically* this does do side effects but i will use it like it does not.
def get_args(obj):
    tups = obj.bytes
    n = 0
    args = []
    while tups[n][0] == "ADD_ARG":
        args += tups[n][1]
        n+=1
    obj.varnames = args
    obj.arg_num = len(args)
    obj.bytes = obj.bytes[n:] #removes add_arg from the bytes
    return obj
