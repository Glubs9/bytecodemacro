# bytecode macro lib
exposes (a slightly modified version of) the bytecode of a function to allow for run-time modification of python syntax.

# how to use
for a description of how to use and install the program, please go to the docs folder on the github (https://github.com/Glubs9/bytecodemacro).

# cool example to get you excited
this is a cool example to get you excited with what this library could do and the fun you can have
doing it.

```python
@macro(cloop)
def test():
    _ = "for c = 0;c < 10;c+=1"
    print(c)
    _ = "end"
test()
#this prints 1 to 10!
```

please have fun writing your own macros! or just have fun looking at
the examples in docs/examples.py in the github

# todo
	- there is a bug in examples.py that i'm not sure about (probably something about bytecompile)
	- allow for uncompile and the compile packages to be used independently on files for other cool stuff (maybe)
	- increase code re-use
	- add error / semantics checking for the returned bytecode (maybe)
	- add more examples
		- optimization macros?
		- steal from examples of lisp macros
	- byte_compile is just soooooo buggy
		- add handling for newly created variables in byte_compile to use store_fast rather than store_name
		- it doesn't compile in the calling scope so it can lead to some wacky situations (variables not recognized)
	- test and then handle encountering the extended arg instruction in the uncompile package
	- test the (end, 0) tuple is not causing any bugs in the bytecodecompile package
	- i am also still lost on closures and co_freevars so if you could get to that it would
		be helpful
