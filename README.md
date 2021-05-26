# bytecode macro lib
exposes (a slightly modified version of) the bytecode of a function to allow for run-time modification of python syntax.

# how to use
for a description of how to use and install the program, please go to the docs folder on the github (https://github.com/Glubs9/bytecodemacro).

# cool example to get you excited
this is a cool example to get you excited with what this library could do and the fun you can have
doing it.

```python
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
f() #prints 1 2 3 4 5 !
```

please have fun writing your own macros! or just have fun looking at
the examples in docs/examples.py in the github

# basic installation
please read through install.txt for requirements but if you just want to get it installed before
looking through the library the comamnd is.  
```
python3 -m pip install bytecodemacro
```

# todo
	- add error / semantics checking for the returned bytecode (maybe)
	- add more examples
	- order examples.py by ease of understanding
		- so the easy ones to read like constant and add_arg are at the top but the ones
			that are harder like cloop or join are at the bottom
	- fix walrus.py
	- test and then handle encountering the extended arg instruction in the uncompile package
	- i am also still lost on closures and co_freevars
