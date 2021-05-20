from macro_lib import macro, byte_compile, unused_var

#i really gotta do something about all these if statements
    #also this only works with strings but fuck it, thats cool as right now
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
